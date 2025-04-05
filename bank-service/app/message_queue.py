import json
import uuid
import time

from pika import BlockingConnection, ConnectionParameters, BasicProperties

from .config import RABBITMQ_HOST, RABBITMQ_PORT, CALLBACK_QUEUE


class MessageQueueConnectionManager:
    def __init__(self,
                 host: str = RABBITMQ_HOST,
                 port: int = RABBITMQ_PORT,
                 retries: int = 2,
                 interval: int = 3
                 ) -> None:
        self.host = host
        self.port = port
        self.retries = retries
        self.interval = interval
        self.connection = None
        self.channel = None

    def connect(self):
        retries = 0

        while True:
            try:
                self.connection = BlockingConnection(
                    ConnectionParameters(
                        host=self.host,
                        port=self.port
                    )
                )
                self.channel = self.connection.channel()

                return self.connection, self.channel
            except Exception as e:
                if retries >= self.retries:
                    raise

                retries += 1
                print(f"Connection failed: {e}")
                time.sleep(self.interval * retries)

    def close(self) -> None:
        if self.channel:
            self.channel.close()

        if self.connection:
            self.connection.close()


class MessageQueue:
    def __init__(self,
                 host=RABBITMQ_HOST,
                 port=RABBITMQ_PORT,
                 exchange_name: str = 'topic_exchange',
                 exchange_type: str = 'topic',
                 reply_queue: str = CALLBACK_QUEUE,
                 timeout: int = 2
                 ):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.reply_queue = reply_queue
        self.timeout = timeout
        self.connection_manager = MessageQueueConnectionManager()

    def connect(self):
        self.connection, self.channel = self.connection_manager.connect()

    def close(self):
        self.connection_manager.close()

    def setup_mq(self):
        self.connect()
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=self.exchange_type
        )

    def on_reply(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            # Assigning the response is crucial part of the consuming process
            # Until responce is none and timeout is not reached, the main thread will be blocked
            self.response = body
            self.delivery_tag = method.delivery_tag

    def setup_reply_queue(self):
        self.channel.queue_declare(self.reply_queue)
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_consume(
            queue=self.reply_queue,
            on_message_callback=self.on_reply
            # auto_ack=True
        )

    def get_reply_message(self):
        start_time = time.time()
        self.response = None

        while self.response is None:
            self.connection.process_data_events(time_limit=0.1)

            if time.time() - start_time > self.timeout:
                print("No reply from server")
                # self.channel.basic_nack()
                return None

        print("received:", self.response)
        self.channel.basic_ack(delivery_tag=self.delivery_tag)
        return self.response.decode()

    def send_message(self, message: dict, routing_key: str, need_reply: bool = False):
        self.setup_mq()

        with self.channel, self.connection:
            message = json.dumps(message)

            if need_reply:
                self.setup_reply_queue()

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message.encode(),

                # If need_reply is True, then set reply_to and correlation_id
                properties=BasicProperties(
                    reply_to=self.reply_queue,
                    correlation_id=self.corr_id
                ) if need_reply else None
            )
            print("sent:", message)

            if need_reply:
                return self.get_reply_message()

            return None
