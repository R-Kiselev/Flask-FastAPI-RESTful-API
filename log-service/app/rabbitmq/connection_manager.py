import asyncio
from typing import (
    Optional,
    Tuple
)

from aio_pika import connect
from aio_pika import (
    Connection,
    Channel,
)
from aio_pika.exceptions import AMQPConnectionError, AMQPError

from ..logging import logger

class MessageQueueConnectionManager:
    def __init__(self,
                 uri: str = None,
                 retries: int = None,
                 interval: int = None) -> None:
        self.uri: str = uri
        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None
        self.max_retries: int = retries
        self.interval: int = interval

    async def connect(self) -> Tuple[Connection, Channel]:
        retries = 0

        while True:
            try:
                self.connection = await connect(self.uri)
                self.channel = await self.connection.channel()

                logger.info("Connected to RabbitMQ")
                return self.connection, self.channel

            except (AMQPConnectionError, AMQPError) as e:
                # Retry connection if max retries not exceeded
                if retries >= self.max_retries:
                    logger.critical(
                        "Failed to connect to RabbitMQ. Max retries exceeded. Error: %s", e)
                    raise
                logger.error("Connection attempt failed with error: %s", e)
                retries += 1

                logger.info("Retrying connection in %s seconds",
                            self.interval * retries)
                await asyncio.sleep(self.interval * retries)

    async def close(self) -> None:
        if self.channel:
            await self.channel.close()
            logger.info("Closed RabbitMQ channel")
        if self.connection:
            await self.connection.close()
            logger.info("Closed RabbitMQ connection")
