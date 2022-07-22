import collections
import inspect
import logging
from typing import Any, Callable, Dict, Optional, Tuple, Union, overload

from fastapi import APIRouter, FastAPI
from starlette.requests import Request
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

from ray import cloudpickle
from ray.dag import DAGNode
from ray.util.annotations import PublicAPI
from ray._private.utils import deprecated

from ray.serve.application import Application
from ray.serve.client import ServeControllerClient
from ray.serve.config import AutoscalingConfig, DeploymentConfig, HTTPOptions
from ray.serve.constants import (
    CONTROLLER_MAX_CONCURRENCY,
    DEFAULT_HTTP_HOST,
    DEFAULT_HTTP_PORT,
)
from ray.serve.context import (
    ReplicaContext,
    get_global_client,
    get_internal_replica_context,
    set_global_client,
)
from ray.serve.deployment import Deployment
from ray.serve.deployment_graph import ClassNode, FunctionNode
from ray.serve.deployment_graph_build import build as pipeline_build
from ray.serve.deployment_graph_build import get_and_validate_ingress_deployment
from ray.serve.exceptions import RayServeException
from ray.serve.handle import RayServeHandle
from ray.serve.http_util import ASGIHTTPSender, make_fastapi_class_based_view
from ray.serve.logging_utils import LoggingContext
from ray.serve.utils import (
    DEFAULT,
    ensure_serialization_context,
    in_interactive_shell,
    install_serve_encoders_to_fastapi,
)

from ray.serve._private import api as _private_api

logger = logging.getLogger(__file__)


@deprecated(instructions="Please see https://docs.ray.io/en/latest/serve/index.html")
@PublicAPI(stability="beta")
def start(
    detached: bool = False,
    http_options: Optional[Union[dict, HTTPOptions]] = None,
    dedicated_cpu: bool = False,
    **kwargs,
) -> ServeControllerClient:
    """Initialize a serve instance.

    By default, the instance will be scoped to the lifetime of the returned
    Client object (or when the script exits). If detached is set to True, the
    instance will instead persist until serve.shutdown() is called. This is
    only relevant if connecting to a long-running Ray cluster (e.g., with
    ray.init(address="auto") or ray.init("ray://<remote_addr>")).

    Args:
        detached: Whether not the instance should be detached from this
          script. If set, the instance will live on the Ray cluster until it is
          explicitly stopped with serve.shutdown().
        http_options (Optional[Dict, serve.HTTPOptions]): Configuration options
          for HTTP proxy. You can pass in a dictionary or HTTPOptions object
          with fields:

            - host(str, None): Host for HTTP servers to listen on. Defaults to
              "127.0.0.1". To expose Serve publicly, you probably want to set
              this to "0.0.0.0".
            - port(int): Port for HTTP server. Defaults to 8000.
            - root_path(str): Root path to mount the serve application
              (for example, "/serve"). All deployment routes will be prefixed
              with this path. Defaults to "".
            - middlewares(list): A list of Starlette middlewares that will be
              applied to the HTTP servers in the cluster. Defaults to [].
            - location(str, serve.config.DeploymentMode): The deployment
              location of HTTP servers:

                - "HeadOnly": start one HTTP server on the head node. Serve
                  assumes the head node is the node you executed serve.start
                  on. This is the default.
                - "EveryNode": start one HTTP server per node.
                - "NoServer" or None: disable HTTP server.
            - num_cpus (int): The number of CPU cores to reserve for each
              internal Serve HTTP proxy actor.  Defaults to 0.
        dedicated_cpu: Whether to reserve a CPU core for the internal
          Serve controller actor.  Defaults to False.
    """

    return _private_api.serve_start(
        detached, http_options, dedicated_cpu, _checkpoint_path, **kwargs
    )


@PublicAPI
def shutdown() -> None:
    """Completely shut down the connected Serve instance.

    Shuts down all processes and deletes all state associated with the
    instance.
    """

    try:
        client = get_global_client()
    except RayServeException:
        logger.info(
            "Nothing to shut down. There's no Serve application "
            "running on this Ray cluster."
        )
        return

    client.shutdown()
    set_global_client(None)


@PublicAPI
def get_replica_context() -> ReplicaContext:
    """If called from a deployment, returns the deployment and replica tag.

    A replica tag uniquely identifies a single replica for a Ray Serve
    deployment at runtime.  Replica tags are of the form
    `<deployment_name>#<random letters>`.

    Raises:
        RayServeException: if not called from within a Ray Serve deployment.

    Example:
        >>> from ray import serve
        >>> # deployment_name
        >>> serve.get_replica_context().deployment # doctest: +SKIP
        >>> # deployment_name#krcwoa
        >>> serve.get_replica_context().replica_tag # doctest: +SKIP
    """
    internal_replica_context = get_internal_replica_context()
    if internal_replica_context is None:
        raise RayServeException(
            "`serve.get_replica_context()` "
            "may only be called from within a "
            "Ray Serve deployment."
        )
    return internal_replica_context


@PublicAPI(stability="beta")
def ingress(app: Union["FastAPI", "APIRouter", Callable]):
    """Mark an ASGI application ingress for Serve.

    Args:
        app (FastAPI,APIRouter,Starlette,etc): the app or router object serve
            as ingress for this deployment. It can be any ASGI compatible
            object.

    Example:
        >>> from fastapi import FastAPI
        >>> from ray import serve
        >>> app = FastAPI() # doctest: +SKIP
        >>> app = FastAPI() # doctest: +SKIP
        >>> @serve.deployment # doctest: +SKIP
        ... @serve.ingress(app) # doctest: +SKIP
        ... class App: # doctest: +SKIP
        ...     pass # doctest: +SKIP
        >>> App.deploy() # doctest: +SKIP
    """

    def decorator(cls):
        if not inspect.isclass(cls):
            raise ValueError("@serve.ingress must be used with a class.")

        if issubclass(cls, collections.abc.Callable):
            raise ValueError(
                "Class passed to @serve.ingress may not have __call__ method."
            )

        # Sometimes there are decorators on the methods. We want to fix
        # the fast api routes here.
        if isinstance(app, (FastAPI, APIRouter)):
            make_fastapi_class_based_view(app, cls)

        # Free the state of the app so subsequent modification won't affect
        # this ingress deployment. We don't use copy.copy here to avoid
        # recursion issue.
        ensure_serialization_context()
        frozen_app = cloudpickle.loads(cloudpickle.dumps(app))

        class ASGIAppWrapper(cls):
            async def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                install_serve_encoders_to_fastapi()

                self._serve_app = frozen_app

                # Use uvicorn's lifespan handling code to properly deal with
                # startup and shutdown event.
                self._serve_asgi_lifespan = LifespanOn(
                    Config(self._serve_app, lifespan="on")
                )
                # Replace uvicorn logger with our own.
                self._serve_asgi_lifespan.logger = logger
                # LifespanOn's logger logs in INFO level thus becomes spammy
                # Within this block we temporarily uplevel for cleaner logging
                with LoggingContext(
                    self._serve_asgi_lifespan.logger, level=logging.WARNING
                ):
                    await self._serve_asgi_lifespan.startup()

            async def __call__(self, request: Request):
                sender = ASGIHTTPSender()
                await self._serve_app(
                    request.scope,
                    request.receive,
                    sender,
                )
                return sender.build_asgi_response()

            # NOTE: __del__ must be async so that we can run asgi shutdown
            # in the same event loop.
            async def __del__(self):
                # LifespanOn's logger logs in INFO level thus becomes spammy
                # Within this block we temporarily uplevel for cleaner logging
                with LoggingContext(
                    self._serve_asgi_lifespan.logger, level=logging.WARNING
                ):
                    await self._serve_asgi_lifespan.shutdown()

                # Make sure to call user's del method as well.
                super_cls = super()
                if hasattr(super_cls, "__del__"):
                    super_cls.__del__()

        ASGIAppWrapper.__name__ = cls.__name__
        return ASGIAppWrapper

    return decorator


@overload
def deployment(func_or_class: Callable) -> Deployment:
    pass


@overload
def deployment(
    name: Optional[str] = None,
    version: Optional[str] = None,
    num_replicas: Optional[int] = None,
    init_args: Optional[Tuple[Any]] = None,
    init_kwargs: Optional[Dict[Any, Any]] = None,
    route_prefix: Union[str, None, DEFAULT] = DEFAULT.VALUE,
    ray_actor_options: Optional[Dict] = None,
    user_config: Optional[Any] = None,
    max_concurrent_queries: Optional[int] = None,
    autoscaling_config: Optional[Union[Dict, AutoscalingConfig]] = None,
    graceful_shutdown_wait_loop_s: Optional[float] = None,
    graceful_shutdown_timeout_s: Optional[float] = None,
    health_check_period_s: Optional[float] = None,
    health_check_timeout_s: Optional[float] = None,
) -> Callable[[Callable], Deployment]:
    pass


@PublicAPI
def deployment(
    _func_or_class: Optional[Callable] = None,
    name: Optional[str] = None,
    version: Optional[str] = None,
    num_replicas: Optional[int] = None,
    init_args: Optional[Tuple[Any]] = None,
    init_kwargs: Optional[Dict[Any, Any]] = None,
    route_prefix: Union[str, None, DEFAULT] = DEFAULT.VALUE,
    ray_actor_options: Optional[Dict] = None,
    user_config: Optional[Any] = None,
    max_concurrent_queries: Optional[int] = None,
    autoscaling_config: Optional[Union[Dict, AutoscalingConfig]] = None,
    graceful_shutdown_wait_loop_s: Optional[float] = None,
    graceful_shutdown_timeout_s: Optional[float] = None,
    health_check_period_s: Optional[float] = None,
    health_check_timeout_s: Optional[float] = None,
) -> Callable[[Callable], Deployment]:
    """Define a Serve deployment.

    Args:
        name (Optional[str]): Globally-unique name identifying this deployment.
            If not provided, the name of the class or function will be used.
        version (Optional[str]): Version of the deployment. This is used to
            indicate a code change for the deployment; when it is re-deployed
            with a version change, a rolling update of the replicas will be
            performed. If not provided, every deployment will be treated as a
            new version.
        num_replicas (Optional[int]): The number of processes to start up that
            will handle requests to this deployment. Defaults to 1.
        init_args (Optional[Tuple]): Positional args to be passed to the class
            constructor when starting up deployment replicas. These can also be
            passed when you call `.deploy()` on the returned Deployment.
        init_kwargs (Optional[Dict]): Keyword args to be passed to the class
            constructor when starting up deployment replicas. These can also be
            passed when you call `.deploy()` on the returned Deployment.
        route_prefix (Optional[str]): Requests to paths under this HTTP path
            prefix will be routed to this deployment. Defaults to '/{name}'.
            When set to 'None', no HTTP endpoint will be created.
            Routing is done based on longest-prefix match, so if you have
            deployment A with a prefix of '/a' and deployment B with a prefix
            of '/a/b', requests to '/a', '/a/', and '/a/c' go to A and requests
            to '/a/b', '/a/b/', and '/a/b/c' go to B. Routes must not end with
            a '/' unless they're the root (just '/'), which acts as a
            catch-all.
        ray_actor_options: Options to be passed to the Ray actor
            constructor such as resource requirements.
        user_config (Optional[Any]): Config to pass to the
            reconfigure method of the deployment. This can be updated
            dynamically without changing the version of the deployment and
            restarting its replicas. The user_config needs to be hashable to
            keep track of updates, so it must only contain hashable types, or
            hashable types nested in lists and dictionaries.
        max_concurrent_queries (Optional[int]): The maximum number of queries
            that will be sent to a replica of this deployment without receiving
            a response. Defaults to 100.

    Example:
    >>> from ray import serve
    >>> @serve.deployment(name="deployment1", version="v1") # doctest: +SKIP
    ... class MyDeployment: # doctest: +SKIP
    ...     pass # doctest: +SKIP

    >>> MyDeployment.deploy(*init_args) # doctest: +SKIP
    >>> MyDeployment.options( # doctest: +SKIP
    ...     num_replicas=2, init_args=init_args).deploy()

    Returns:
        Deployment
    """

    # Num of replicas should not be 0.
    # TODO(Sihan) seperate num_replicas attribute from internal and api
    if num_replicas == 0:
        raise ValueError("num_replicas is expected to larger than 0")

    if num_replicas is not None and autoscaling_config is not None:
        raise ValueError(
            "Manually setting num_replicas is not allowed when "
            "autoscaling_config is provided."
        )

    config = DeploymentConfig.from_default(
        ignore_none=True,
        num_replicas=num_replicas,
        user_config=user_config,
        max_concurrent_queries=max_concurrent_queries,
        autoscaling_config=autoscaling_config,
        graceful_shutdown_wait_loop_s=graceful_shutdown_wait_loop_s,
        graceful_shutdown_timeout_s=graceful_shutdown_timeout_s,
        health_check_period_s=health_check_period_s,
        health_check_timeout_s=health_check_timeout_s,
    )

    def decorator(_func_or_class):
        return Deployment(
            _func_or_class,
            name if name is not None else _func_or_class.__name__,
            config,
            version=version,
            init_args=init_args,
            init_kwargs=init_kwargs,
            route_prefix=route_prefix,
            ray_actor_options=ray_actor_options,
            _internal=True,
        )

    # This handles both parametrized and non-parametrized usage of the
    # decorator. See the @serve.batch code for more details.
    return decorator(_func_or_class) if callable(_func_or_class) else decorator


@deprecated(instructions="Please see https://docs.ray.io/en/latest/serve/index.html")
@PublicAPI
def get_deployment(name: str) -> Deployment:
    """Dynamically fetch a handle to a Deployment object.

    This can be used to update and redeploy a deployment without access to
    the original definition.

    Example:
    >>> from ray import serve
    >>> MyDeployment = serve.get_deployment("name")  # doctest: +SKIP
    >>> MyDeployment.options(num_replicas=10).deploy()  # doctest: +SKIP

    Args:
        name(str): name of the deployment. This must have already been
        deployed.

    Returns:
        Deployment
    """
    return _private_api.get_deployment(name)


@deprecated(instructions="Please see https://docs.ray.io/en/latest/serve/index.html")
@PublicAPI
def list_deployments() -> Dict[str, Deployment]:
    """Returns a dictionary of all active deployments.

    Dictionary maps deployment name to Deployment objects.
    """

    return _private_api.list_deployments()


@PublicAPI(stability="alpha")
def run(
    target: Union[ClassNode, FunctionNode],
    _blocking: bool = True,
    *,
    host: str = DEFAULT_HTTP_HOST,
    port: int = DEFAULT_HTTP_PORT,
) -> Optional[RayServeHandle]:
    """Run a Serve application and return a ServeHandle to the ingress.

    Either a ClassNode, FunctionNode, or a pre-built application
    can be passed in. If a node is passed in, all of the deployments it depends
    on will be deployed. If there is an ingress, its handle will be returned.

    Args:
        target (Union[ClassNode, FunctionNode, Application]):
            A user-built Serve Application or a ClassNode that acts as the
            root node of DAG. By default ClassNode is the Driver
            deployment unless user provides a customized one.
        host: The host passed into serve.start().
        port: The port passed into serve.start().

    Returns:
        RayServeHandle: A regular ray serve handle that can be called by user
            to execute the serve DAG.
    """

    client = _private_api.serve_start(
        detached=True, http_options={"host": host, "port": port}
    )

    if isinstance(target, Application):
        deployments = list(target.deployments.values())
        ingress = target.ingress
    # Each DAG should always provide a valid Driver ClassNode
    elif isinstance(target, ClassNode):
        deployments = pipeline_build(target)
        ingress = get_and_validate_ingress_deployment(deployments)
    # Special case where user is doing single function serve.run(func.bind())
    elif isinstance(target, FunctionNode):
        deployments = pipeline_build(target)
        ingress = get_and_validate_ingress_deployment(deployments)
        if len(deployments) != 1:
            raise ValueError(
                "We only support single function node in serve.run, ex: "
                "serve.run(func.bind()). For more than one nodes in your DAG, "
                "Please provide a driver class and bind it as entrypoint to "
                "your Serve DAG."
            )
    elif isinstance(target, DAGNode):
        raise ValueError(
            "Invalid DAGNode type as entry to serve.run(), "
            f"type: {type(target)}, accepted: ClassNode, "
            "FunctionNode please provide a driver class and bind it "
            "as entrypoint to your Serve DAG."
        )
    else:
        raise TypeError(
            "Expected a ClassNode, FunctionNode, or Application as target. "
            f"Got unexpected type {type(target)} instead."
        )

    parameter_group = []

    for deployment in deployments:
        deployment_parameters = {
            "name": deployment._name,
            "func_or_class": deployment._func_or_class,
            "init_args": deployment.init_args,
            "init_kwargs": deployment.init_kwargs,
            "ray_actor_options": deployment._ray_actor_options,
            "config": deployment._config,
            "version": deployment._version,
            "route_prefix": deployment.route_prefix,
            "url": deployment.url,
        }
        parameter_group.append(deployment_parameters)
    client.deploy_group(
        parameter_group, _blocking=_blocking, remove_past_deployments=True
    )

    if ingress is not None:
        return ingress._get_handle()


def build(target: Union[ClassNode, FunctionNode]) -> Application:
    """Builds a Serve application into a static application.

    Takes in a ClassNode or FunctionNode and converts it to a
    Serve application consisting of one or more deployments. This is intended
    to be used for production scenarios and deployed via the Serve REST API or
    CLI, so there are some restrictions placed on the deployments:
        1) All of the deployments must be importable. That is, they cannot be
           defined in __main__ or inline defined. The deployments will be
           imported in production using the same import path they were here.
        2) All arguments bound to the deployment must be JSON-serializable.

    The returned Application object can be exported to a dictionary or YAML
    config.
    """

    if in_interactive_shell():
        raise RuntimeError(
            "build cannot be called from an interactive shell like "
            "IPython or Jupyter because it requires all deployments to be "
            "importable to run the app after building."
        )

    # TODO(edoakes): this should accept host and port, but we don't
    # currently support them in the REST API.
    return Application(pipeline_build(target))
