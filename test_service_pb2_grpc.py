# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import test_service_pb2 as src_dot_ray_dot_protobuf_dot_test__service__pb2


class TestServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
            "/ray.rpc.TestService/Ping",
            request_serializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingRequest.SerializeToString,
            response_deserializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingReply.FromString,
        )
        self.PingTimeout = channel.unary_unary(
            "/ray.rpc.TestService/PingTimeout",
            request_serializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutRequest.SerializeToString,
            response_deserializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutReply.FromString,
        )


class TestServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PingTimeout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TestServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Ping": grpc.unary_unary_rpc_method_handler(
            servicer.Ping,
            request_deserializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingRequest.FromString,
            response_serializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingReply.SerializeToString,
        ),
        "PingTimeout": grpc.unary_unary_rpc_method_handler(
            servicer.PingTimeout,
            request_deserializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutRequest.FromString,
            response_serializer=src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "ray.rpc.TestService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class TestService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ray.rpc.TestService/Ping",
            src_dot_ray_dot_protobuf_dot_test__service__pb2.PingRequest.SerializeToString,
            src_dot_ray_dot_protobuf_dot_test__service__pb2.PingReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PingTimeout(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ray.rpc.TestService/PingTimeout",
            src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutRequest.SerializeToString,
            src_dot_ray_dot_protobuf_dot_test__service__pb2.PingTimeoutReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
