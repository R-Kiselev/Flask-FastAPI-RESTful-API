import os
import json
from dotenv import load_dotenv

from pydantic import AmqpDsn, EmailStr
from pydantic_settings import BaseSettings

from .logging import logger


load_dotenv()


class EmailSettings(BaseSettings):
    # SMTP SSL Port (ex. 465)
    email_port: int = int(os.getenv("email_port", "465"))

    # SMTP host (ex. smtp.gmail.com)
    email_host: str = os.getenv("email_host", "smtp.gmail.com")

    # SMTP Login credentials
    email_user: EmailStr = os.getenv(
        "email_user", "your_email_address@gmail.com")

    # Check readme for more info
    email_app_password: str = os.getenv(
        "email_app_password", "abcd abcd abcd abcd")

    # Receivers, can be multiple.
    # Contains a string with comma separated email addresses
    email_receivers: str = os.getenv(
        "email_receivers", "address@gmail.com, example@gmail.com")

    # Theme of the email
    email_subject: str = os.getenv(
        "email_subject", "Message from Bank service")


class AppSettings(BaseSettings):
    '''Custom configuration class for centralizing app settings'''

    amqp_dsn: AmqpDsn = os.getenv(
        'AMQP_URI', 'amqp://guest:guest@rabbitmq:5672'
    )
    queue_name: str = os.getenv('QUEUE_NAME', 'email-service')
    exchange_name: str = os.getenv('EXCHANGE_NAME', 'topic_exchange')
    routing_key: str = os.getenv('ROUTING_KEY', '*.created')


email_settings = EmailSettings()
app_settings = AppSettings()
