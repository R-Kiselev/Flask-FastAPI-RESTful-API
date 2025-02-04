import os
from dotenv import load_dotenv
from pydantic import (
    MongoDsn,
    AmqpDsn,
    field_validator
)
from pydantic_settings import BaseSettings

from .logging import logger

load_dotenv()


class Settings(BaseSettings):
    '''Custom configuration class for centralizing app settings'''

    mongodb_dsn: MongoDsn = os.getenv(
        'MONGODB_URI', 'mongodb://mongodb:27017'
    )
    mongodb_name: str = os.getenv('MONGODB_NAME', 'log-service')
    mongodb_collections: set[str] = set(
        os.getenv('MONGODB_COLLECTIONS', 'logs').split(',')
    )

    amqp_dsn: AmqpDsn = os.getenv(
        'AMQP_URI', 'amqp://guest:guest@rabbitmq:5672'
    )
    queue_name: str = os.getenv('QUEUE_NAME', 'log-service')

    @field_validator('mongodb_collections')
    def validate_collections(cls, collections):
        if not collections:
            logger.error("mongodb_collections cannot be empty")
            raise ValueError("mongodb_collections cannot be empty")
        return collections

    def get_mongodb_collection(cls, name: str):
        if name not in cls.mongodb_collections:
            logger.error(f" Collection {name} not found")
            raise ValueError(f"Collection {name} not found")
        return name


settings = Settings()
