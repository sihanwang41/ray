# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/ray/protobuf/serve.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1csrc/ray/protobuf/serve.proto\x12\tray.serve\"\xb6\x03\n\x11\x41utoscalingConfig\x12\x14\n\x0cmin_replicas\x18\x01 \x01(\r\x12\x14\n\x0cmax_replicas\x18\x02 \x01(\r\x12/\n\'target_num_ongoing_requests_per_replica\x18\x03 \x01(\x01\x12\x1a\n\x12metrics_interval_s\x18\x04 \x01(\x01\x12\x1a\n\x12look_back_period_s\x18\x05 \x01(\x01\x12\x18\n\x10smoothing_factor\x18\x06 \x01(\x01\x12\x19\n\x11\x64ownscale_delay_s\x18\x07 \x01(\x01\x12\x17\n\x0fupscale_delay_s\x18\x08 \x01(\x01\x12\x1d\n\x10initial_replicas\x18\t \x01(\rH\x00\x88\x01\x01\x12%\n\x18upscale_smoothing_factor\x18\n \x01(\x01H\x01\x88\x01\x01\x12\'\n\x1a\x64ownscale_smoothing_factor\x18\x0b \x01(\x01H\x02\x88\x01\x01\x42\x13\n\x11_initial_replicasB\x1b\n\x19_upscale_smoothing_factorB\x1d\n\x1b_downscale_smoothing_factor\"\xb0\x03\n\x10\x44\x65ploymentConfig\x12\x14\n\x0cnum_replicas\x18\x01 \x01(\x05\x12\x1e\n\x16max_concurrent_queries\x18\x02 \x01(\x05\x12\x13\n\x0buser_config\x18\x03 \x01(\x0c\x12%\n\x1dgraceful_shutdown_wait_loop_s\x18\x04 \x01(\x01\x12#\n\x1bgraceful_shutdown_timeout_s\x18\x05 \x01(\x01\x12\x1d\n\x15health_check_period_s\x18\x06 \x01(\x01\x12\x1e\n\x16health_check_timeout_s\x18\x07 \x01(\x01\x12\x19\n\x11is_cross_language\x18\x08 \x01(\x08\x12:\n\x13\x64\x65ployment_language\x18\t \x01(\x0e\x32\x1d.ray.serve.DeploymentLanguage\x12\x38\n\x12\x61utoscaling_config\x18\n \x01(\x0b\x32\x1c.ray.serve.AutoscalingConfig\x12\x0f\n\x07version\x18\x0b \x01(\t\x12$\n\x1cuser_configured_option_names\x18\x0c \x03(\t\"\xb6\x01\n\x0fRequestMetadata\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x10\n\x08\x65ndpoint\x18\x02 \x01(\t\x12\x13\n\x0b\x63\x61ll_method\x18\x03 \x01(\t\x12\x38\n\x07\x63ontext\x18\x04 \x03(\x0b\x32\'.ray.serve.RequestMetadata.ContextEntry\x1a.\n\x0c\x43ontextEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x1e\n\x0eRequestWrapper\x12\x0c\n\x04\x62ody\x18\x01 \x01(\x0c\"=\n\rUpdatedObject\x12\x17\n\x0fobject_snapshot\x18\x01 \x01(\x0c\x12\x13\n\x0bsnapshot_id\x18\x02 \x01(\x05\"\x9c\x01\n\x0fLongPollRequest\x12O\n\x14keys_to_snapshot_ids\x18\x01 \x03(\x0b\x32\x31.ray.serve.LongPollRequest.KeysToSnapshotIdsEntry\x1a\x38\n\x16KeysToSnapshotIdsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\xa9\x01\n\x0eLongPollResult\x12\x46\n\x0fupdated_objects\x18\x01 \x03(\x0b\x32-.ray.serve.LongPollResult.UpdatedObjectsEntry\x1aO\n\x13UpdatedObjectsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\'\n\x05value\x18\x02 \x01(\x0b\x32\x18.ray.serve.UpdatedObject:\x02\x38\x01\"\x98\x01\n\x0c\x45ndpointInfo\x12\x15\n\rendpoint_name\x18\x01 \x01(\t\x12\r\n\x05route\x18\x02 \x01(\t\x12\x33\n\x06\x63onfig\x18\x03 \x03(\x0b\x32#.ray.serve.EndpointInfo.ConfigEntry\x1a-\n\x0b\x43onfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x92\x01\n\x0b\x45ndpointSet\x12\x38\n\tendpoints\x18\x01 \x03(\x0b\x32%.ray.serve.EndpointSet.EndpointsEntry\x1aI\n\x0e\x45ndpointsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.ray.serve.EndpointInfo:\x02\x38\x01\"\x1e\n\rActorNameList\x12\r\n\x05names\x18\x01 \x03(\t\"\xde\x01\n\x11\x44\x65ploymentVersion\x12\x14\n\x0c\x63ode_version\x18\x01 \x01(\t\x12\x36\n\x11\x64\x65ployment_config\x18\x02 \x01(\x0b\x32\x1b.ray.serve.DeploymentConfig\x12\x19\n\x11ray_actor_options\x18\x03 \x01(\t\x12\x1f\n\x17placement_group_bundles\x18\x04 \x01(\t\x12 \n\x18placement_group_strategy\x18\x05 \x01(\t\x12\x1d\n\x15max_replicas_per_node\x18\x06 \x01(\x05\"\xe9\x01\n\rReplicaConfig\x12\x1b\n\x13\x64\x65ployment_def_name\x18\x01 \x01(\t\x12\x16\n\x0e\x64\x65ployment_def\x18\x02 \x01(\x0c\x12\x11\n\tinit_args\x18\x03 \x01(\x0c\x12\x13\n\x0binit_kwargs\x18\x04 \x01(\x0c\x12\x19\n\x11ray_actor_options\x18\x05 \x01(\t\x12\x1f\n\x17placement_group_bundles\x18\x06 \x01(\t\x12 \n\x18placement_group_strategy\x18\x07 \x01(\t\x12\x1d\n\x15max_replicas_per_node\x18\x08 \x01(\x05\"\xd9\x01\n\x0e\x44\x65ploymentInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x36\n\x11\x64\x65ployment_config\x18\x02 \x01(\x0b\x32\x1b.ray.serve.DeploymentConfig\x12\x30\n\x0ereplica_config\x18\x03 \x01(\x0b\x32\x18.ray.serve.ReplicaConfig\x12\x15\n\rstart_time_ms\x18\x04 \x01(\x03\x12\x12\n\nactor_name\x18\x05 \x01(\t\x12\x0f\n\x07version\x18\x06 \x01(\t\x12\x13\n\x0b\x65nd_time_ms\x18\x07 \x01(\x03\"T\n\x0f\x44\x65ploymentRoute\x12\x32\n\x0f\x64\x65ployment_info\x18\x01 \x01(\x0b\x32\x19.ray.serve.DeploymentInfo\x12\r\n\x05route\x18\x02 \x01(\t\"L\n\x13\x44\x65ploymentRouteList\x12\x35\n\x11\x64\x65ployment_routes\x18\x01 \x03(\x0b\x32\x1a.ray.serve.DeploymentRoute\"b\n\x14\x44\x65ploymentStatusInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\x06status\x18\x02 \x01(\x0e\x32\x1b.ray.serve.DeploymentStatus\x12\x0f\n\x07message\x18\x03 \x01(\t\"\\\n\x18\x44\x65ploymentStatusInfoList\x12@\n\x17\x64\x65ployment_status_infos\x18\x01 \x03(\x0b\x32\x1f.ray.serve.DeploymentStatusInfo\"t\n\x15\x41pplicationStatusInfo\x12,\n\x06status\x18\x01 \x01(\x0e\x32\x1c.ray.serve.ApplicationStatus\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1c\n\x14\x64\x65ployment_timestamp\x18\x03 \x01(\x01\"\x96\x01\n\x0eStatusOverview\x12\x34\n\napp_status\x18\x01 \x01(\x0b\x32 .ray.serve.ApplicationStatusInfo\x12@\n\x13\x64\x65ployment_statuses\x18\x02 \x01(\x0b\x32#.ray.serve.DeploymentStatusInfoList\x12\x0c\n\x04name\x18\x03 \x01(\t\"s\n\x0ePredictRequest\x12\x33\n\x05input\x18\x02 \x03(\x0b\x32$.ray.serve.PredictRequest.InputEntry\x1a,\n\nInputEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x38\x01\"%\n\x0fPredictResponse\x12\x12\n\nprediction\x18\x01 \x01(\x0c\"\x19\n\x17ListApplicationsRequest\"5\n\x18ListApplicationsResponse\x12\x19\n\x11\x61pplication_names\x18\x01 \x03(\t\"\x10\n\x0eHealthzRequest\"\"\n\x0fHealthzResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"<\n\x12UserDefinedMessage\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x66oo\x18\x02 \x01(\t\x12\x0b\n\x03num\x18\x03 \x01(\x03\"7\n\x13UserDefinedResponse\x12\x10\n\x08greeting\x18\x01 \x01(\t\x12\x0e\n\x06num_x2\x18\x02 \x01(\x03\"\x15\n\x13UserDefinedMessage2\"(\n\x14UserDefinedResponse2\x12\x10\n\x08greeting\x18\x01 \x01(\t\"=\n\x0c\x46ruitAmounts\x12\x0e\n\x06orange\x18\x01 \x01(\x03\x12\r\n\x05\x61pple\x18\x02 \x01(\x03\x12\x0e\n\x06\x62\x61nana\x18\x03 \x01(\x03\"\x1b\n\nFruitCosts\x12\r\n\x05\x63osts\x18\x01 \x01(\x02\"\x17\n\x07RawData\x12\x0c\n\x04nums\x18\x01 \x03(\x02\"\x1d\n\x0bModelOutput\x12\x0e\n\x06output\x18\x01 \x01(\x02**\n\x12\x44\x65ploymentLanguage\x12\n\n\x06PYTHON\x10\x00\x12\x08\n\x04JAVA\x10\x01*r\n\x10\x44\x65ploymentStatus\x12\x1e\n\x1a\x44\x45PLOYMENT_STATUS_UPDATING\x10\x00\x12\x1d\n\x19\x44\x45PLOYMENT_STATUS_HEALTHY\x10\x01\x12\x1f\n\x1b\x44\x45PLOYMENT_STATUS_UNHEALTHY\x10\x02*\xe2\x01\n\x11\x41pplicationStatus\x12 \n\x1c\x41PPLICATION_STATUS_DEPLOYING\x10\x00\x12\x1e\n\x1a\x41PPLICATION_STATUS_RUNNING\x10\x01\x12$\n APPLICATION_STATUS_DEPLOY_FAILED\x10\x02\x12\x1f\n\x1b\x41PPLICATION_STATUS_DELETING\x10\x03\x12\"\n\x1e\x41PPLICATION_STATUS_NOT_STARTED\x10\x05\x12 \n\x1c\x41PPLICATION_STATUS_UNHEALTHY\x10\x06\x32V\n\x12PredictAPIsService\x12@\n\x07Predict\x12\x19.ray.serve.PredictRequest\x1a\x1a.ray.serve.PredictResponse2\xb3\x01\n\x12RayServeAPIService\x12[\n\x10ListApplications\x12\".ray.serve.ListApplicationsRequest\x1a#.ray.serve.ListApplicationsResponse\x12@\n\x07Healthz\x12\x19.ray.serve.HealthzRequest\x1a\x1a.ray.serve.HealthzResponse2\xc3\x02\n\x12UserDefinedService\x12I\n\x08__call__\x12\x1d.ray.serve.UserDefinedMessage\x1a\x1e.ray.serve.UserDefinedResponse\x12H\n\x07Method1\x12\x1d.ray.serve.UserDefinedMessage\x1a\x1e.ray.serve.UserDefinedResponse\x12J\n\x07Method2\x12\x1e.ray.serve.UserDefinedMessage2\x1a\x1f.ray.serve.UserDefinedResponse2\x12L\n\tStreaming\x12\x1d.ray.serve.UserDefinedMessage\x1a\x1e.ray.serve.UserDefinedResponse0\x01\x32L\n\x0c\x46ruitService\x12<\n\nFruitStand\x12\x17.ray.serve.FruitAmounts\x1a\x15.ray.serve.FruitCosts2S\n\x18RayServeBenchmarkService\x12\x37\n\tgrpc_call\x12\x12.ray.serve.RawData\x1a\x16.ray.serve.ModelOutputB*\n\x16io.ray.serve.generatedB\x0bServeProtosP\x01\xf8\x01\x01\x62\x06proto3')

_DEPLOYMENTLANGUAGE = DESCRIPTOR.enum_types_by_name['DeploymentLanguage']
DeploymentLanguage = enum_type_wrapper.EnumTypeWrapper(_DEPLOYMENTLANGUAGE)
_DEPLOYMENTSTATUS = DESCRIPTOR.enum_types_by_name['DeploymentStatus']
DeploymentStatus = enum_type_wrapper.EnumTypeWrapper(_DEPLOYMENTSTATUS)
_APPLICATIONSTATUS = DESCRIPTOR.enum_types_by_name['ApplicationStatus']
ApplicationStatus = enum_type_wrapper.EnumTypeWrapper(_APPLICATIONSTATUS)
PYTHON = 0
JAVA = 1
DEPLOYMENT_STATUS_UPDATING = 0
DEPLOYMENT_STATUS_HEALTHY = 1
DEPLOYMENT_STATUS_UNHEALTHY = 2
APPLICATION_STATUS_DEPLOYING = 0
APPLICATION_STATUS_RUNNING = 1
APPLICATION_STATUS_DEPLOY_FAILED = 2
APPLICATION_STATUS_DELETING = 3
APPLICATION_STATUS_NOT_STARTED = 5
APPLICATION_STATUS_UNHEALTHY = 6


_AUTOSCALINGCONFIG = DESCRIPTOR.message_types_by_name['AutoscalingConfig']
_DEPLOYMENTCONFIG = DESCRIPTOR.message_types_by_name['DeploymentConfig']
_REQUESTMETADATA = DESCRIPTOR.message_types_by_name['RequestMetadata']
_REQUESTMETADATA_CONTEXTENTRY = _REQUESTMETADATA.nested_types_by_name['ContextEntry']
_REQUESTWRAPPER = DESCRIPTOR.message_types_by_name['RequestWrapper']
_UPDATEDOBJECT = DESCRIPTOR.message_types_by_name['UpdatedObject']
_LONGPOLLREQUEST = DESCRIPTOR.message_types_by_name['LongPollRequest']
_LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY = _LONGPOLLREQUEST.nested_types_by_name['KeysToSnapshotIdsEntry']
_LONGPOLLRESULT = DESCRIPTOR.message_types_by_name['LongPollResult']
_LONGPOLLRESULT_UPDATEDOBJECTSENTRY = _LONGPOLLRESULT.nested_types_by_name['UpdatedObjectsEntry']
_ENDPOINTINFO = DESCRIPTOR.message_types_by_name['EndpointInfo']
_ENDPOINTINFO_CONFIGENTRY = _ENDPOINTINFO.nested_types_by_name['ConfigEntry']
_ENDPOINTSET = DESCRIPTOR.message_types_by_name['EndpointSet']
_ENDPOINTSET_ENDPOINTSENTRY = _ENDPOINTSET.nested_types_by_name['EndpointsEntry']
_ACTORNAMELIST = DESCRIPTOR.message_types_by_name['ActorNameList']
_DEPLOYMENTVERSION = DESCRIPTOR.message_types_by_name['DeploymentVersion']
_REPLICACONFIG = DESCRIPTOR.message_types_by_name['ReplicaConfig']
_DEPLOYMENTINFO = DESCRIPTOR.message_types_by_name['DeploymentInfo']
_DEPLOYMENTROUTE = DESCRIPTOR.message_types_by_name['DeploymentRoute']
_DEPLOYMENTROUTELIST = DESCRIPTOR.message_types_by_name['DeploymentRouteList']
_DEPLOYMENTSTATUSINFO = DESCRIPTOR.message_types_by_name['DeploymentStatusInfo']
_DEPLOYMENTSTATUSINFOLIST = DESCRIPTOR.message_types_by_name['DeploymentStatusInfoList']
_APPLICATIONSTATUSINFO = DESCRIPTOR.message_types_by_name['ApplicationStatusInfo']
_STATUSOVERVIEW = DESCRIPTOR.message_types_by_name['StatusOverview']
_PREDICTREQUEST = DESCRIPTOR.message_types_by_name['PredictRequest']
_PREDICTREQUEST_INPUTENTRY = _PREDICTREQUEST.nested_types_by_name['InputEntry']
_PREDICTRESPONSE = DESCRIPTOR.message_types_by_name['PredictResponse']
_LISTAPPLICATIONSREQUEST = DESCRIPTOR.message_types_by_name['ListApplicationsRequest']
_LISTAPPLICATIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListApplicationsResponse']
_HEALTHZREQUEST = DESCRIPTOR.message_types_by_name['HealthzRequest']
_HEALTHZRESPONSE = DESCRIPTOR.message_types_by_name['HealthzResponse']
_USERDEFINEDMESSAGE = DESCRIPTOR.message_types_by_name['UserDefinedMessage']
_USERDEFINEDRESPONSE = DESCRIPTOR.message_types_by_name['UserDefinedResponse']
_USERDEFINEDMESSAGE2 = DESCRIPTOR.message_types_by_name['UserDefinedMessage2']
_USERDEFINEDRESPONSE2 = DESCRIPTOR.message_types_by_name['UserDefinedResponse2']
_FRUITAMOUNTS = DESCRIPTOR.message_types_by_name['FruitAmounts']
_FRUITCOSTS = DESCRIPTOR.message_types_by_name['FruitCosts']
_RAWDATA = DESCRIPTOR.message_types_by_name['RawData']
_MODELOUTPUT = DESCRIPTOR.message_types_by_name['ModelOutput']
AutoscalingConfig = _reflection.GeneratedProtocolMessageType('AutoscalingConfig', (_message.Message,), {
  'DESCRIPTOR' : _AUTOSCALINGCONFIG,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.AutoscalingConfig)
  })
_sym_db.RegisterMessage(AutoscalingConfig)

DeploymentConfig = _reflection.GeneratedProtocolMessageType('DeploymentConfig', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTCONFIG,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentConfig)
  })
_sym_db.RegisterMessage(DeploymentConfig)

RequestMetadata = _reflection.GeneratedProtocolMessageType('RequestMetadata', (_message.Message,), {

  'ContextEntry' : _reflection.GeneratedProtocolMessageType('ContextEntry', (_message.Message,), {
    'DESCRIPTOR' : _REQUESTMETADATA_CONTEXTENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.RequestMetadata.ContextEntry)
    })
  ,
  'DESCRIPTOR' : _REQUESTMETADATA,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.RequestMetadata)
  })
_sym_db.RegisterMessage(RequestMetadata)
_sym_db.RegisterMessage(RequestMetadata.ContextEntry)

RequestWrapper = _reflection.GeneratedProtocolMessageType('RequestWrapper', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTWRAPPER,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.RequestWrapper)
  })
_sym_db.RegisterMessage(RequestWrapper)

UpdatedObject = _reflection.GeneratedProtocolMessageType('UpdatedObject', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDOBJECT,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.UpdatedObject)
  })
_sym_db.RegisterMessage(UpdatedObject)

LongPollRequest = _reflection.GeneratedProtocolMessageType('LongPollRequest', (_message.Message,), {

  'KeysToSnapshotIdsEntry' : _reflection.GeneratedProtocolMessageType('KeysToSnapshotIdsEntry', (_message.Message,), {
    'DESCRIPTOR' : _LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.LongPollRequest.KeysToSnapshotIdsEntry)
    })
  ,
  'DESCRIPTOR' : _LONGPOLLREQUEST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.LongPollRequest)
  })
_sym_db.RegisterMessage(LongPollRequest)
_sym_db.RegisterMessage(LongPollRequest.KeysToSnapshotIdsEntry)

LongPollResult = _reflection.GeneratedProtocolMessageType('LongPollResult', (_message.Message,), {

  'UpdatedObjectsEntry' : _reflection.GeneratedProtocolMessageType('UpdatedObjectsEntry', (_message.Message,), {
    'DESCRIPTOR' : _LONGPOLLRESULT_UPDATEDOBJECTSENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.LongPollResult.UpdatedObjectsEntry)
    })
  ,
  'DESCRIPTOR' : _LONGPOLLRESULT,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.LongPollResult)
  })
_sym_db.RegisterMessage(LongPollResult)
_sym_db.RegisterMessage(LongPollResult.UpdatedObjectsEntry)

EndpointInfo = _reflection.GeneratedProtocolMessageType('EndpointInfo', (_message.Message,), {

  'ConfigEntry' : _reflection.GeneratedProtocolMessageType('ConfigEntry', (_message.Message,), {
    'DESCRIPTOR' : _ENDPOINTINFO_CONFIGENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.EndpointInfo.ConfigEntry)
    })
  ,
  'DESCRIPTOR' : _ENDPOINTINFO,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.EndpointInfo)
  })
_sym_db.RegisterMessage(EndpointInfo)
_sym_db.RegisterMessage(EndpointInfo.ConfigEntry)

EndpointSet = _reflection.GeneratedProtocolMessageType('EndpointSet', (_message.Message,), {

  'EndpointsEntry' : _reflection.GeneratedProtocolMessageType('EndpointsEntry', (_message.Message,), {
    'DESCRIPTOR' : _ENDPOINTSET_ENDPOINTSENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.EndpointSet.EndpointsEntry)
    })
  ,
  'DESCRIPTOR' : _ENDPOINTSET,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.EndpointSet)
  })
_sym_db.RegisterMessage(EndpointSet)
_sym_db.RegisterMessage(EndpointSet.EndpointsEntry)

ActorNameList = _reflection.GeneratedProtocolMessageType('ActorNameList', (_message.Message,), {
  'DESCRIPTOR' : _ACTORNAMELIST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ActorNameList)
  })
_sym_db.RegisterMessage(ActorNameList)

DeploymentVersion = _reflection.GeneratedProtocolMessageType('DeploymentVersion', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTVERSION,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentVersion)
  })
_sym_db.RegisterMessage(DeploymentVersion)

ReplicaConfig = _reflection.GeneratedProtocolMessageType('ReplicaConfig', (_message.Message,), {
  'DESCRIPTOR' : _REPLICACONFIG,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ReplicaConfig)
  })
_sym_db.RegisterMessage(ReplicaConfig)

DeploymentInfo = _reflection.GeneratedProtocolMessageType('DeploymentInfo', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTINFO,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentInfo)
  })
_sym_db.RegisterMessage(DeploymentInfo)

DeploymentRoute = _reflection.GeneratedProtocolMessageType('DeploymentRoute', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTROUTE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentRoute)
  })
_sym_db.RegisterMessage(DeploymentRoute)

DeploymentRouteList = _reflection.GeneratedProtocolMessageType('DeploymentRouteList', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTROUTELIST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentRouteList)
  })
_sym_db.RegisterMessage(DeploymentRouteList)

DeploymentStatusInfo = _reflection.GeneratedProtocolMessageType('DeploymentStatusInfo', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSTATUSINFO,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentStatusInfo)
  })
_sym_db.RegisterMessage(DeploymentStatusInfo)

DeploymentStatusInfoList = _reflection.GeneratedProtocolMessageType('DeploymentStatusInfoList', (_message.Message,), {
  'DESCRIPTOR' : _DEPLOYMENTSTATUSINFOLIST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.DeploymentStatusInfoList)
  })
_sym_db.RegisterMessage(DeploymentStatusInfoList)

ApplicationStatusInfo = _reflection.GeneratedProtocolMessageType('ApplicationStatusInfo', (_message.Message,), {
  'DESCRIPTOR' : _APPLICATIONSTATUSINFO,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ApplicationStatusInfo)
  })
_sym_db.RegisterMessage(ApplicationStatusInfo)

StatusOverview = _reflection.GeneratedProtocolMessageType('StatusOverview', (_message.Message,), {
  'DESCRIPTOR' : _STATUSOVERVIEW,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.StatusOverview)
  })
_sym_db.RegisterMessage(StatusOverview)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), {

  'InputEntry' : _reflection.GeneratedProtocolMessageType('InputEntry', (_message.Message,), {
    'DESCRIPTOR' : _PREDICTREQUEST_INPUTENTRY,
    '__module__' : 'ray.serve.generated.serve_pb2'
    # @@protoc_insertion_point(class_scope:ray.serve.PredictRequest.InputEntry)
    })
  ,
  'DESCRIPTOR' : _PREDICTREQUEST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.PredictRequest)
  })
_sym_db.RegisterMessage(PredictRequest)
_sym_db.RegisterMessage(PredictRequest.InputEntry)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTRESPONSE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.PredictResponse)
  })
_sym_db.RegisterMessage(PredictResponse)

ListApplicationsRequest = _reflection.GeneratedProtocolMessageType('ListApplicationsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTAPPLICATIONSREQUEST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ListApplicationsRequest)
  })
_sym_db.RegisterMessage(ListApplicationsRequest)

ListApplicationsResponse = _reflection.GeneratedProtocolMessageType('ListApplicationsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTAPPLICATIONSRESPONSE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ListApplicationsResponse)
  })
_sym_db.RegisterMessage(ListApplicationsResponse)

HealthzRequest = _reflection.GeneratedProtocolMessageType('HealthzRequest', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHZREQUEST,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.HealthzRequest)
  })
_sym_db.RegisterMessage(HealthzRequest)

HealthzResponse = _reflection.GeneratedProtocolMessageType('HealthzResponse', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHZRESPONSE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.HealthzResponse)
  })
_sym_db.RegisterMessage(HealthzResponse)

UserDefinedMessage = _reflection.GeneratedProtocolMessageType('UserDefinedMessage', (_message.Message,), {
  'DESCRIPTOR' : _USERDEFINEDMESSAGE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.UserDefinedMessage)
  })
_sym_db.RegisterMessage(UserDefinedMessage)

UserDefinedResponse = _reflection.GeneratedProtocolMessageType('UserDefinedResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERDEFINEDRESPONSE,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.UserDefinedResponse)
  })
_sym_db.RegisterMessage(UserDefinedResponse)

UserDefinedMessage2 = _reflection.GeneratedProtocolMessageType('UserDefinedMessage2', (_message.Message,), {
  'DESCRIPTOR' : _USERDEFINEDMESSAGE2,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.UserDefinedMessage2)
  })
_sym_db.RegisterMessage(UserDefinedMessage2)

UserDefinedResponse2 = _reflection.GeneratedProtocolMessageType('UserDefinedResponse2', (_message.Message,), {
  'DESCRIPTOR' : _USERDEFINEDRESPONSE2,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.UserDefinedResponse2)
  })
_sym_db.RegisterMessage(UserDefinedResponse2)

FruitAmounts = _reflection.GeneratedProtocolMessageType('FruitAmounts', (_message.Message,), {
  'DESCRIPTOR' : _FRUITAMOUNTS,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.FruitAmounts)
  })
_sym_db.RegisterMessage(FruitAmounts)

FruitCosts = _reflection.GeneratedProtocolMessageType('FruitCosts', (_message.Message,), {
  'DESCRIPTOR' : _FRUITCOSTS,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.FruitCosts)
  })
_sym_db.RegisterMessage(FruitCosts)

RawData = _reflection.GeneratedProtocolMessageType('RawData', (_message.Message,), {
  'DESCRIPTOR' : _RAWDATA,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.RawData)
  })
_sym_db.RegisterMessage(RawData)

ModelOutput = _reflection.GeneratedProtocolMessageType('ModelOutput', (_message.Message,), {
  'DESCRIPTOR' : _MODELOUTPUT,
  '__module__' : 'ray.serve.generated.serve_pb2'
  # @@protoc_insertion_point(class_scope:ray.serve.ModelOutput)
  })
_sym_db.RegisterMessage(ModelOutput)

_PREDICTAPISSERVICE = DESCRIPTOR.services_by_name['PredictAPIsService']
_RAYSERVEAPISERVICE = DESCRIPTOR.services_by_name['RayServeAPIService']
_USERDEFINEDSERVICE = DESCRIPTOR.services_by_name['UserDefinedService']
_FRUITSERVICE = DESCRIPTOR.services_by_name['FruitService']
_RAYSERVEBENCHMARKSERVICE = DESCRIPTOR.services_by_name['RayServeBenchmarkService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026io.ray.serve.generatedB\013ServeProtosP\001\370\001\001'
  _REQUESTMETADATA_CONTEXTENTRY._options = None
  _REQUESTMETADATA_CONTEXTENTRY._serialized_options = b'8\001'
  _LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY._options = None
  _LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY._serialized_options = b'8\001'
  _LONGPOLLRESULT_UPDATEDOBJECTSENTRY._options = None
  _LONGPOLLRESULT_UPDATEDOBJECTSENTRY._serialized_options = b'8\001'
  _ENDPOINTINFO_CONFIGENTRY._options = None
  _ENDPOINTINFO_CONFIGENTRY._serialized_options = b'8\001'
  _ENDPOINTSET_ENDPOINTSENTRY._options = None
  _ENDPOINTSET_ENDPOINTSENTRY._serialized_options = b'8\001'
  _PREDICTREQUEST_INPUTENTRY._options = None
  _PREDICTREQUEST_INPUTENTRY._serialized_options = b'8\001'
  _DEPLOYMENTLANGUAGE._serialized_start=3800
  _DEPLOYMENTLANGUAGE._serialized_end=3842
  _DEPLOYMENTSTATUS._serialized_start=3844
  _DEPLOYMENTSTATUS._serialized_end=3958
  _APPLICATIONSTATUS._serialized_start=3961
  _APPLICATIONSTATUS._serialized_end=4187
  _AUTOSCALINGCONFIG._serialized_start=44
  _AUTOSCALINGCONFIG._serialized_end=482
  _DEPLOYMENTCONFIG._serialized_start=485
  _DEPLOYMENTCONFIG._serialized_end=917
  _REQUESTMETADATA._serialized_start=920
  _REQUESTMETADATA._serialized_end=1102
  _REQUESTMETADATA_CONTEXTENTRY._serialized_start=1056
  _REQUESTMETADATA_CONTEXTENTRY._serialized_end=1102
  _REQUESTWRAPPER._serialized_start=1104
  _REQUESTWRAPPER._serialized_end=1134
  _UPDATEDOBJECT._serialized_start=1136
  _UPDATEDOBJECT._serialized_end=1197
  _LONGPOLLREQUEST._serialized_start=1200
  _LONGPOLLREQUEST._serialized_end=1356
  _LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY._serialized_start=1300
  _LONGPOLLREQUEST_KEYSTOSNAPSHOTIDSENTRY._serialized_end=1356
  _LONGPOLLRESULT._serialized_start=1359
  _LONGPOLLRESULT._serialized_end=1528
  _LONGPOLLRESULT_UPDATEDOBJECTSENTRY._serialized_start=1449
  _LONGPOLLRESULT_UPDATEDOBJECTSENTRY._serialized_end=1528
  _ENDPOINTINFO._serialized_start=1531
  _ENDPOINTINFO._serialized_end=1683
  _ENDPOINTINFO_CONFIGENTRY._serialized_start=1638
  _ENDPOINTINFO_CONFIGENTRY._serialized_end=1683
  _ENDPOINTSET._serialized_start=1686
  _ENDPOINTSET._serialized_end=1832
  _ENDPOINTSET_ENDPOINTSENTRY._serialized_start=1759
  _ENDPOINTSET_ENDPOINTSENTRY._serialized_end=1832
  _ACTORNAMELIST._serialized_start=1834
  _ACTORNAMELIST._serialized_end=1864
  _DEPLOYMENTVERSION._serialized_start=1867
  _DEPLOYMENTVERSION._serialized_end=2089
  _REPLICACONFIG._serialized_start=2092
  _REPLICACONFIG._serialized_end=2325
  _DEPLOYMENTINFO._serialized_start=2328
  _DEPLOYMENTINFO._serialized_end=2545
  _DEPLOYMENTROUTE._serialized_start=2547
  _DEPLOYMENTROUTE._serialized_end=2631
  _DEPLOYMENTROUTELIST._serialized_start=2633
  _DEPLOYMENTROUTELIST._serialized_end=2709
  _DEPLOYMENTSTATUSINFO._serialized_start=2711
  _DEPLOYMENTSTATUSINFO._serialized_end=2809
  _DEPLOYMENTSTATUSINFOLIST._serialized_start=2811
  _DEPLOYMENTSTATUSINFOLIST._serialized_end=2903
  _APPLICATIONSTATUSINFO._serialized_start=2905
  _APPLICATIONSTATUSINFO._serialized_end=3021
  _STATUSOVERVIEW._serialized_start=3024
  _STATUSOVERVIEW._serialized_end=3174
  _PREDICTREQUEST._serialized_start=3176
  _PREDICTREQUEST._serialized_end=3291
  _PREDICTREQUEST_INPUTENTRY._serialized_start=3247
  _PREDICTREQUEST_INPUTENTRY._serialized_end=3291
  _PREDICTRESPONSE._serialized_start=3293
  _PREDICTRESPONSE._serialized_end=3330
  _LISTAPPLICATIONSREQUEST._serialized_start=3332
  _LISTAPPLICATIONSREQUEST._serialized_end=3357
  _LISTAPPLICATIONSRESPONSE._serialized_start=3359
  _LISTAPPLICATIONSRESPONSE._serialized_end=3412
  _HEALTHZREQUEST._serialized_start=3414
  _HEALTHZREQUEST._serialized_end=3430
  _HEALTHZRESPONSE._serialized_start=3432
  _HEALTHZRESPONSE._serialized_end=3466
  _USERDEFINEDMESSAGE._serialized_start=3468
  _USERDEFINEDMESSAGE._serialized_end=3528
  _USERDEFINEDRESPONSE._serialized_start=3530
  _USERDEFINEDRESPONSE._serialized_end=3585
  _USERDEFINEDMESSAGE2._serialized_start=3587
  _USERDEFINEDMESSAGE2._serialized_end=3608
  _USERDEFINEDRESPONSE2._serialized_start=3610
  _USERDEFINEDRESPONSE2._serialized_end=3650
  _FRUITAMOUNTS._serialized_start=3652
  _FRUITAMOUNTS._serialized_end=3713
  _FRUITCOSTS._serialized_start=3715
  _FRUITCOSTS._serialized_end=3742
  _RAWDATA._serialized_start=3744
  _RAWDATA._serialized_end=3767
  _MODELOUTPUT._serialized_start=3769
  _MODELOUTPUT._serialized_end=3798
  _PREDICTAPISSERVICE._serialized_start=4189
  _PREDICTAPISSERVICE._serialized_end=4275
  _RAYSERVEAPISERVICE._serialized_start=4278
  _RAYSERVEAPISERVICE._serialized_end=4457
  _USERDEFINEDSERVICE._serialized_start=4460
  _USERDEFINEDSERVICE._serialized_end=4783
  _FRUITSERVICE._serialized_start=4785
  _FRUITSERVICE._serialized_end=4861
  _RAYSERVEBENCHMARKSERVICE._serialized_start=4863
  _RAYSERVEBENCHMARKSERVICE._serialized_end=4946
# @@protoc_insertion_point(module_scope)
