import asyncio

from .message_queue import MessageQueueServer
from ..logging import logger
from ..config import app_settings


class MessageQueueRunner:
    async def start_messages_listener(self):
        logger.info('Initializing message listener.')
        self.mqserver = MessageQueueServer(
            uri = str(app_settings.amqp_dsn),
            queue_name = app_settings.queue_name,
            exchange_name = app_settings.exchange_name,
            routing_key = app_settings.routing_key
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
