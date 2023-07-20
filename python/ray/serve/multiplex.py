import asyncio
from collections import OrderedDict
import inspect
import logging
import threading
import time
from typing import Any, Callable, List, Set

from ray._private.async_compat import sync_to_async
from ray.serve._private.constants import (
    SERVE_LOGGER_NAME,
    PUSH_MULTIPLEXED_MODEL_IDS_INTERVAL_S,
)
from ray.serve.context import (
    get_global_client,
    get_internal_replica_context,
)
from ray.serve._private.common import MultiplexedReplicaInfo
from ray.serve import metrics
from ray._private.utils import get_or_create_event_loop


logger = logging.getLogger(SERVE_LOGGER_NAME)


class _ModelMultiplexWrapper:
    """A wrapper class that wraps the model load function and
    provides the LRU caching functionality.

    The model multiplexer is a wrapper class that wraps the model load function
    and provides the LRU caching functionality, and the model load function should
    be a coroutine function that takes the model ID as the first argument and
    returns the user-constructed model object.
    The model multiplexer will also ensure that the number of models on the current
    replica does not exceed the specified limit.
    The model will be unloaded in the LRU order, the model multiplexer will call the
    model's __del__ attribute if it exists to clean up the model resources eagerly.

    """

    def __init__(
        self,
        model_load_func: Callable[[str], Any],
        self_arg: Any,
        max_num_models_per_replica: int,
    ):
        """Initialize the model multiplexer.
        Args:
            model_load_func: the model load async function.
            self_arg: self argument when model_load_func is class method.
            max_num_models_per_replica: the maximum number of models to be loaded on the
                current replica. If it is -1, there is no limit for the number of models
                per replica.
        """
        self.models = OrderedDict()
        self._func: Callable = model_load_func
        self.self_arg: Any = self_arg
        self.max_num_models_per_replica: int = max_num_models_per_replica

        self.model_load_latency_s = metrics.Gauge(
            "serve_multiplexed_model_load_latency_s",
            description="The time it takes to load a model.",
        )
        self.model_unload_latency_s = metrics.Gauge(
            "serve_multiplexed_model_unload_latency_s",
            description="The time it takes to unload a model.",
        )
        self.num_models = metrics.Gauge(
            "serve_num_multiplexed_models",
            description="The number of models loaded on the current replica.",
        )

        self.models_unload_counter = metrics.Counter(
            "serve_multiplexed_models_unload_counter",
            description="The counter for unloaded models on the current replica.",
        )
        self.models_load_counter = metrics.Counter(
            "serve_multiplexed_models_load_counter",
            description="The counter for loaded models on the current replica.",
        )

        context = get_internal_replica_context()
        if context is None:
            raise RuntimeError(
                "Fail to retrieve serve replica context, the model multiplexer ",
                "can only be used within `Deployment`.",
            )
        self._deployment_name: str = context.deployment
        self._replica_tag: str = context.replica_tag

        # Whether to push the multiplexed replica info to the controller.
        self._push_multiplexed_replica_info: bool = False

        # Model cache lock
        self._model_cache_lock = asyncio.Lock()
        self._model_load_tasks: Set[str] = set()
        self._model_ids_pusher_thread_stop: bool = False
        # Push the model IDs to the controller periodically.
        self._model_ids_pusher_thread = threading.Thread(target=self._push_model_ids)
        self._model_ids_pusher_thread.setDaemon(True)
        self._model_ids_pusher_thread.start()

    async def load_model(self, model_id: str) -> Any:
        """Load the model if it is not loaded yet, and return the user-constructed model object.

        Args:
            model_id: the model ID.

        Returns:
            The user-constructed model object.
        """

        if type(model_id) != str:
            raise TypeError("The model ID must be a string.")

        if not model_id:
            raise ValueError("The model ID cannot be empty.")

        self.num_models.set(len(self.models))
        if model_id in self.models:
            # Move the model to the end of the OrderedDict to ensure LRU caching.
            model = self.models.pop(model_id)
            self.models[model_id] = model
            return self.models[model_id]
        else:
            self._push_multiplexed_replica_info = True
            self._model_load_tasks.add(model_id)
            async with self._model_cache_lock:
                # Check if the model has been loaded by another request.
                if model_id in self.models:
                    return self.models[model_id]

                # If the number of models per replica is specified, check if
                # the number of models on the current replica has reached the limit.
                if (
                    self.max_num_models_per_replica > 0
                    and len(self.models) >= self.max_num_models_per_replica
                ):
                    # Unload the least recently used model.
                    self.models_unload_counter.inc()
                    unload_start_time = time.time()
                    await self.unload_model()
                    self.model_unload_latency_s.set(time.time() - unload_start_time)

                # Load the model.
                logger.info(f"Loading model '{model_id}'.")
                self.models_load_counter.inc()
                load_start_time = time.time()
                if self.self_arg is None:
                    self.models[model_id] = await self._func(model_id)
                else:
                    self.models[model_id] = await self._func(self.self_arg, model_id)
                self._push_multiplexed_replica_info = True
                self._model_load_tasks.discard(model_id)
                self.model_load_latency_s.set(time.time() - load_start_time)
                return self.models[model_id]

    async def unload_model(self) -> None:
        """Unload the least recently used model."""
        model_id, model = self.models.popitem(last=False)
        logger.info(f"Unloading model '{model_id}'.")

        # If the model has __del__ attribute, call it.
        # This is to clean up the model resources eagerly.
        if hasattr(model, "__del__"):
            if not inspect.iscoroutinefunction(model.__del__):
                await asyncio.get_running_loop().run_in_executor(None, model.__del__)
            else:
                await sync_to_async(model.__del__)()
            setattr(model, "__del__", lambda _: None)

    def _get_model_ids(self) -> List[str]:
        """Get the model IDs of the models loaded & loading on the current replica."""
        models_list = set(self.models.keys())
        models_list.update(self._model_load_tasks)
        return list(models_list)

    def _push_model_ids(self):
        """Push the multiplexed replica info to the controller."""

        while True:
            try:
                if self._model_ids_pusher_thread_stop:
                    break
                if self._push_multiplexed_replica_info:
                    get_global_client().record_multiplexed_replica_info(
                        MultiplexedReplicaInfo(
                            self._deployment_name,
                            self._replica_tag,
                            self._get_model_ids(),
                        )
                    )
                    self._push_multiplexed_replica_info = False
            except Exception as e:
                logger.warning(
                    "Failed to push the multiplexed replica info "
                    f"to the controller. Error: {e}"
                )
            time.sleep(PUSH_MULTIPLEXED_MODEL_IDS_INTERVAL_S)

    def __del__(self):
        while len(self.models) > 0:
            asyncio.run(self.unload_model())
        self._model_ids_pusher_thread_stop = True
        self._model_ids_pusher_thread.join()
