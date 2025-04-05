from aiosmtplib import SMTP

import ssl

from email.message import EmailMessage
from .config import email_settings
from .logging import logger


async def send_email(data: dict = None, subject: str = None) -> None:
    message = EmailMessage()
    message["Subject"] = subject if subject else email_settings.email_subject
    message["From"] = email_settings.email_user
    message["To"] = email_settings.email_receivers
    message.set_content(f"Message: {data}")

    # establishing an encrypted connection between a server and a client
    context = ssl.create_default_context()

    try:
        async with SMTP(
            hostname=email_settings.email_host,
            port=email_settings.email_port,
            use_tls=True,
            tls_context=context
        ) as server:
            # ehlo() is the SMTP command the client uses to tell the server that it is an SMTP client
            await server.ehlo()
            await server.login(email_settings.email_user, email_settings.email_app_password)
            await server.send_message(message)
            logger.info(f'Email sent successfully: {\
                message.get_content(), message["To"], message["Subject"]}')

    except Exception as e:
        logger.error(f'Error sending email: {e}')
        raise e
