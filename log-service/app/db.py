from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings
from .logging import logger

async def connect_and_init_db():
    global db_client
    try:
        mongodb_uri = str(settings.mongodb_dsn)
        db_client = AsyncIOMotorClient(mongodb_uri)
        
        logger.info(f'Connected to mongo at {mongodb_uri}')
    except Exception as e:
        logger.error(f'Error connecting to mongo: {e}')
        raise


async def get_db_client() -> AsyncIOMotorClient:
    """ Usage:
    - db = Depends(get_db_client) - in FastAPI route
    - db = await get_db_client() - in async function
    """
    db_name = settings.mongodb_name
    return db_client[db_name]


async def close_db_connection():
    global db_client
    if db_client is None:
        logger.info('No connection to close.')
        return
    db_client.close()
    db_client = None
    logger.info('Connection closed.')
