import requests
import logging
from ray import serve

#  __json_start__


@serve.deployment(logging_config={"encoding": "JSON"})
class Model:
    def __call__(self) -> int:
        return "hello world"


# __json_end__

serve.run(Model.bind())

resp = requests.get("http://localhost:8000/")


#  __level_start__


@serve.deployment(logging_config={"log_level": "DEBUG"})
class Model:
    def __call__(self) -> int:
        logger = logging.getLogger("ray.serve")
        logger.debug("this is debug message")
        return "hello world"


# __level_end__

serve.run(Model.bind())

resp = requests.get("http://localhost:8000/")


# __logs_dir_start__
@serve.deployment(logging_config={"logs_dir": "/my_dirs"})
class Model:
    def __call__(self) -> int:
        return "hello world"


# __logs_dir_end__


# __enable_access_log_start__
@serve.deployment(logging_config={"enable_access_log": False})
class Model:
    def __call__(self) -> int:
        logger = logging.getLogger("ray.serve")
        logger.info("hello world")
        return


# __enable_access_log_end__

serve.run(Model.bind())

resp = requests.get("http://localhost:8000/")


# __application_and_deployment_start__
@serve.deployment
class Router:
    def __init__(self, handle):
        self.handle = handle

    async def __call__(self):
        logger = logging.getLogger("ray.serve")
        logger.debug("this is debug message from router")
        return await self.handle.remote()


@serve.deployment
class Model:
    def __call__(self) -> int:
        logger = logging.getLogger("ray.serve")
        logger.debug("this is debug message from model")
        return "hello world"


serve.run(Router.bind(Model.bind()), logging_config={"log_level": "DEBUG"})
resp = requests.get("http://localhost:8000/")
# __application_and_deployment_end__

# __configure_serve_component_start__
serve.start(system_logging_config={"log_level": "DEBUG"})
# __configure_serve_component_end__
