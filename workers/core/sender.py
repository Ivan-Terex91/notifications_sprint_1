import os
from abc import ABC
from typing import Any

from python_http_client.client import Response
from sendgrid import Mail, SendGridAPIClient
from core.logger import logger


class Sender(ABC):
    async def send(self, message: Any):
        pass


class EmailSender(Sender):
    def __init__(self, client: Any):
        self.client = client

    async def send(self, message: Any) -> Response:
        response = self.client.send(message)
        return response


class SendgridService(EmailSender):
    """Сервис отправки сообщений"""

    def __init__(self, client: SendGridAPIClient):
        super().__init__(client)

    async def send(self, message: Any) -> None:
        email = Mail(
            from_email=os.getenv("FROM_EMAIL", "oguseynov@yandex.ru"),
            to_emails=message.email,
            subject=message.subject,
            plain_text_content=message.text,
        )
        self.client.send(email)
        logger.info(msg=f"Sending message {email}")