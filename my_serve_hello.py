from fastapi import FastAPI

from ray import serve

serve.start(detached=True)

app = FastAPI()


@serve.deployment(route_prefix="/")
@serve.ingress(app)
class HelloWorld:
    @app.get("/")
    def hello(self):
        return "Hello world!"

    @app.get("/healthcheck")
    def healthcheck(self):
        return


HelloWorld.deploy()
