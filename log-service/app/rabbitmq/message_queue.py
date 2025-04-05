import json
from typing import (
    Optional,
    Dict,
    Any,
    AsyncGenerator,
)

from aio_pika import ExchangeType
from aio_pika import (
    Connection,
    Channel,
    Queue,
    Exchange,
)
from aio_pika.abc import AbstractIncomingMessage

from ..config import settings
from ..logging import logger
from .connection_manager import MessageQueueConnectionManager
from ..db import get_db_client


RABBITMQ_URL = str(settings.amqp_dsn)


class MessageQueueServer:
    def __init__(self,
                 uri: str = RABBITMQ_URL,
                 queue_name: str = 'email-service',
                 exchange_name: str = 'topic_exchange',
                 routing_key: str = '*.created',
                 exchange_type: ExchangeType = ExchangeType.TOPIC,
                 retries: int = 3,
                 interval: int = 5
                 ) -> None:
        self.uri: str = uri
        self.connection: Optional[Connection] = None
        self.channel: Optional[Channel] = None
        self.queue: Optional[Queue] = None
        self.connection_manager = MessageQueueConnectionManager(
            uri, retries, interval)

        self.exchange: Optional[Exchange] = None
        self.exchange_type: ExchangeType = exchange_type
        self.exchange_name: str = exchange_name
        self.queue_name: str = queue_name
        self.routing_key: str = routing_key

    async def setup_queue(self) -> None:
        """Setup the queue and exchange only once during initialization"""
        self.exchange = await self.channel.declare_exchange(
            name=self.exchange_name,
            type=self.exchange_type
        )
        self.queue = await self.channel.declare_queue(
            name=self.queue_name,
            durable=True
        )
        await self.queue.bind(
            exchange=self.exchange,
            routing_key=self.routing_key
        )

    async def close(self) -> None:
        await self.connection_manager.close()
        self.queue = None

    async def save_message(self, log: Dict[str, Any]) -> None:
        db = await get_db_client()
        db_collection = settings.get_mongodb_collection('logs')

        await db[db_collection].insert_one(log)
        logger.info('Message saved to data storage')

    async def on_message(self, incoming_message: AbstractIncomingMessage) -> Optional[Dict[str, Any]]:
        """Process incoming message and return the decoded message"""
        try:
            decoded_message = incoming_message.body.decode()
            message = json.loads(decoded_message)
            logger.info(f'Processed message content: {message}')

            await incoming_message.ack()
            logger.info('Message acknowledged')

            return message
        except Exception as e:
            logger.error(f'Error processing message: {e}')
            await incoming_message.nack(requeue=True)
            logger.warning('Message nack with requeue')

            return None

    async def get_queue_messages(self) -> AsyncGenerator[Dict[str, Any]]:
        async with self.queue.iterator() as queue_iter:
            async for incoming_message in queue_iter:
                decoded_message = await self.on_message(incoming_message)
                if decoded_message is None:
                    continue

                logger.info('Yielding decoded message')

                # Yield the message because we want to return messages one by one to make code cleaner
                yield decoded_message

    async def listen(self) -> None:
        while True:
            try:
                async for message in self.get_queue_messages():
                    await self.save_message(message)
                    logger.info('listener: saved message')

            except Exception as e:
                # If an error occurs, close the connection and try to reconnect
                logger.error(
                    f"Error in listen loop: {e}. Attempting to reconnect.")
                await self.close()
                try:
                    self.connection, self.channel = await self.connection_manager.connect()
                    await self.setup_queue()

                except Exception as reconnect_e:
                    logger.critical(f"Reconnection failed: {reconnect_e}")
                    break

    async def run(self) -> None:
        self.connection, self.channel = await self.connection_manager.connect()
        await self.setup_queue()
        await self.listen()
