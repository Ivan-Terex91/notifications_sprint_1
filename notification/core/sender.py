import logging
import os
from abc import ABC
from typing import Any

from python_http_client.client import Response
from sendgrid import SendGridAPIClient, Email


class Sender(ABC):
    async def send(self):
        pass


class EmailSender(Sender):
    client: Any

    async def send(self, message: Any) -> Response:
        response = self.client.send(message)
        return response


class Sendgrid(EmailSender):
    client = SendGridAPIClient(
        os.environ.get('SENDGRID_API_KEY', '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'))

    def send(self, message: Email) -> Response:
        try:
            response = self.client.send(message)
            return response
        except Exception as e:
            logging.error(e)
