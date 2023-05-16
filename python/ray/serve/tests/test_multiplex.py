import pytest
from typing import List

import ray
from ray import serve
from ray.serve.multiplex import _ModelMultiplexWrapper
from ray.serve.context import get_internal_replica_context
from ray._private.test_utils import wait_for_condition
from ray.serve._private.common import RunningReplicaInfo


@pytest.fixture()
def start_serve_with_context():
    serve.start()
    ray.serve.context._set_internal_replica_context(
        "fake_deployment", "fake_replica_tag", None, None, None
    )
    yield
    serve.shutdown()


class TestMultiplexWrapper:
    def test_failed_to_get_replica_context(self):
        async def model_load_func(model_id: str):
            return model_id

        with pytest.raises(
            RuntimeError, match="Fail to retrieve serve replica context"
        ):
            _ModelMultiplexWrapper(model_load_func, None, max_num_models_per_replica=2)

    @pytest.mark.asyncio
    async def test_multiplex_wrapper(self, start_serve_with_context):
        """Test multiplex wrapper with LRU caching."""

        async def model_load_func(model_id: str):
            return model_id

        multiplexer = _ModelMultiplexWrapper(
            model_load_func, None, max_num_models_per_replica=2
        )
        # Load model1
        await multiplexer.load_model("1")
        assert multiplexer.models == {"1": "1"}
        # Load model2
        await multiplexer.load_model("2")
        assert multiplexer._push_multiplexed_replica_info is True
        assert multiplexer.models == {"1": "1", "2": "2"}

        # Load model3, model1 should be unloaded
        await multiplexer.load_model("3")
        assert multiplexer._push_multiplexed_replica_info is True
        assert multiplexer.models == {"2": "2", "3": "3"}

        # reload model2, model2 should be moved to the end of the LRU cache
        await multiplexer.load_model("2")
        assert multiplexer._push_multiplexed_replica_info is True
        assert multiplexer.models == {"3": "3", "2": "2"}

        # Load model4, model3 should be unloaded
        await multiplexer.load_model("4")
        assert multiplexer._push_multiplexed_replica_info is True
        assert multiplexer.models == {"2": "2", "4": "4"}

    @pytest.mark.asyncio
    async def test_bad_call_multiplexed_func(self, start_serve_with_context):
        """Test bad call to multiplexed function"""

        async def model_load_func(model_id: str):
            return model_id

        multiplexer = _ModelMultiplexWrapper(
            model_load_func, None, max_num_models_per_replica=2
        )
        with pytest.raises(TypeError):
            await multiplexer.load_model(1)
        with pytest.raises(TypeError):
            await multiplexer.load_model()

    @pytest.mark.asyncio
    async def test_unload_model_call_del(self, start_serve_with_context):
        class MyModel:
            def __init__(self, model_id):
                self.model_id = model_id

            def __del__(self):
                raise Exception(f"{self.model_id} is dead")

            def __eq__(self, model):
                return model.model_id == self.model_id

        async def model_load_func(model_id: str) -> MyModel:
            return MyModel(model_id)

        multiplexer = _ModelMultiplexWrapper(
            model_load_func, None, max_num_models_per_replica=1
        )
        await multiplexer.load_model("1")
        assert multiplexer.models == {"1": MyModel("1")}
        with pytest.raises(Exception, match="1 is dead"):
            await multiplexer.load_model("2")


class TestBasicAPI:
    def test_decorator_validation(self):
        @serve.multiplexed
        async def get_model(model: str):
            return

        @serve.multiplexed(max_num_models_per_replica=1)
        async def get_model2(model: str):
            return

        @serve.deployment
        class MyModel:
            @serve.multiplexed
            async def get_model(model: str):
                return

        @serve.deployment
        class MyModel2:
            @serve.multiplexed(max_num_models_per_replica=1)
            async def get_model(self, model: str):
                return

        # multiplex can only be used with func or method.
        with pytest.raises(TypeError):

            @serve.deployment
            @serve.multiplexed
            class BadDecorator:
                pass

        # max_num_models_per_replica must be an integer
        with pytest.raises(TypeError):

            @serve.multiplexed(max_num_models_per_replica="1")
            async def get_model3(model: str):
                pass

        # max_num_models_per_replica must be positive
        with pytest.raises(ValueError):

            @serve.multiplexed(max_num_models_per_replica=0)
            async def get_model4(model: str):
                pass

        # multiplexed function must be async def
        with pytest.raises(TypeError):

            @serve.multiplexed
            def get_model5(model: str):
                pass

        with pytest.raises(TypeError):

            @serve.deployment
            class MyModel3:
                @serve.multiplexed
                def get_model(self, model: str):
                    return

        # no model_id argument in multiplexed function
        with pytest.raises(TypeError):

            @serve.multiplexed
            def get_model6():
                pass

        with pytest.raises(TypeError):

            @serve.deployment
            class MyModel4:
                @serve.multiplexed
                def get_model(self):
                    return

    def test_get_multiplexed_model_id(self):
        """Test get_multiplexed_model_id() API"""
        assert serve.get_multiplexed_model_id() == ""
        ray.serve.context._serve_request_context.set(
            ray.serve.context.RequestContext(multiplexed_model_id="1")
        )
        assert serve.get_multiplexed_model_id() == "1"


def test_multiplexed_replica_info():
    """Test MultiplexedReplicaInfo is passed to the controller & router"""

    @serve.deployment
    class MyModel:
        @serve.multiplexed(max_num_models_per_replica=2)
        async def get_model(self, model_id: str):
            return

        async def __call__(self, model_id: str):
            _ = await self.get_model(model_id)
            context = get_internal_replica_context()
            return (context.deployment, context.replica_tag)

    handle = serve.run(MyModel.bind())
    deployment, replica_tag = ray.get(handle.remote("model1"))

    def check_replica_information(
        replicas: List[RunningReplicaInfo],
        deployment: str,
        replica_tag: str,
        model_ids: List[str],
    ):
        for replica in replicas:
            assert replica.deployment_name == deployment
            assert replica.replica_tag == replica_tag
            assert list(replica.multiplexed_model_ids) == model_ids
        return True

    wait_for_condition(
        check_replica_information,
        replicas=handle.router._replica_set.in_flight_queries.keys(),
        deployment=deployment,
        replica_tag=replica_tag,
        model_ids=[
            "model1",
        ],
    )

    ray.get(handle.remote("model2"))
    wait_for_condition(
        check_replica_information,
        replicas=handle.router._replica_set.in_flight_queries.keys(),
        deployment=deployment,
        replica_tag=replica_tag,
        model_ids=[
            "model1",
            "model2",
        ],
    )

    # LRU remove the model1
    ray.get(handle.remote("model3"))
    wait_for_condition(
        check_replica_information,
        replicas=handle.router._replica_set.in_flight_queries.keys(),
        deployment=deployment,
        replica_tag=replica_tag,
        model_ids=[
            "model2",
            "model3",
        ],
    )


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main(["-v", "-s", __file__]))
