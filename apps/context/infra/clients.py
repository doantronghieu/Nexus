import packages

from context.infra import services_info

from toolkit.utils import utils
from toolkit.db import mongodb, redix

from qdrant_client import QdrantClient, AsyncQdrantClient
from loguru import logger

#*=============================================================================

error_handler = utils.LocationAwareErrorHandler()
error_handler_silent = utils.LocationAwareErrorHandler(
    utils.CFGS_LOCATION_AWARE_ERROR_HANDLER["silent"]
)

#*=============================================================================
client_qdrant = QdrantClient(
	host=services_info.HOST_QDRANT,
	port=services_info.PORT_QDRANT,
	grpc_port=services_info.PORT_QDRANT + 1,
)

client_qdrant_async = AsyncQdrantClient(
	host=services_info.HOST_QDRANT,
	port=services_info.PORT_QDRANT,
	grpc_port=services_info.PORT_QDRANT + 1,
	# prefer_grpc=True,
	# force_disable_check_same_thread=True,
)

#*=============================================================================

manager_mongodb = mongodb.MongoDBDatabaseManager(
	username="root",
	password="example",
	host=services_info.HOST_MONGODB,
	port="27017",
	db_name="app"
)

mdb_coll_vehicle = manager_mongodb.get_collection("vehicle")

#*=============================================================================

config_redis = redix.RedisConfig(
	host=services_info.HOST_REDIS,
	port=6379,
	password="mypassword",
	db=0
)
manager_redis = redix.RedisDatabaseManager(config_redis)
client_redis = manager_redis.client

namespace_redis_llm = manager_redis.get_namespace("llm")
