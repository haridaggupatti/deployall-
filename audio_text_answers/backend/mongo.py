from pymongo import MongoClient
import redis
import logging

# Setup logging
logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self) -> None:
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

async def redisConnection():
    try:
        redis_client = RedisClient()
        logger.info("Connected to Redis")
        return redis_client.redis_client
    except Exception as e:
        logger.error(f"Error connecting to Redis: {str(e)}")
        raise

mongo_client = None

async def connectdb():
    global mongo_client
    
    if not mongo_client:
        try:
            mongo_client = MongoClient('mongodb://localhost:27017/')
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise

def get_index(index_name):
    if mongo_client:
        return mongo_client[index_name]
    else:
        logger.error("Connect to the database before accessing the index")
        raise Exception("Database connection is not established")

async def dbconnect(index_name, collection_name):
    await connectdb()
    try:
        index_connect = get_index(index_name)
        logger.info(f"Connected to index {index_name}")
        collection_connect = index_connect[collection_name]
        logger.info(f"Connected to collection {collection_name} in index {index_name}")
        return collection_connect
    except Exception as e:
        logger.error(f"Error while connecting to DB collection {collection_name} in index {index_name}: {str(e)}")
        raise
