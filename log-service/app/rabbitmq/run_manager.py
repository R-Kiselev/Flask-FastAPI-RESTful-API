import asyncio

from .message_queue import MessageQueueServer
from ..logging import logger
from ..config import settings


class MessageQueueRunner:
    def __init__(self,
                 uri: str = str(settings.amqp_dsn),
                 queue_name: str = settings.queue_name,
                 exchange_name: str = settings.exchange_name,
                 routing_key: str = settings.routing_key
                 ) -> None:
        self.uri: str = uri
        self.queue_name: str = queue_name
        self.exchange_name: str = exchange_name
        self.routing_key: str = routing_key

    async def start_messages_listener(self):
        logger.info('Initializing message listener.')
        self.mqserver = MessageQueueServer(
            uri=self.uri,
            queue_name=self.queue_name,
            exchange_name=self.exchange_name,
            routing_key=self.routing_key
        )

        logger.info('Starting message listener in background.')
        # Run the message listener in the background because it's an infinite loop
        self.task = asyncio.create_task(self.mqserver.run())

    async def stop_message_listener(self):
        logger.info('Stopping message listener.')
        if self.mqserver:
            await self.mqserver.close()
        if self.task:
            logger.info('Cancelling message listener task.')
            self.task.cancel()
