import asyncio
import os

from pydantic import ValidationError

from core.logger import logger
from core.mongo import MongoService
from core.rabbit import RabbitService
from core.sender import SendgridService
from models import models


class Worker:
    """Класс Worker"""

    def __init__(
        self,
        rabbit_service: RabbitService,
        mongo_service: MongoService,
        sender_service: SendgridService,
        rabbit_task_queue: str,
        mongo_collection: str,
    ):
        """"""
        self.rabbit = rabbit_service
        self.mongo = mongo_service
        self.sender = sender_service
        self.task_queue = rabbit_task_queue
        self.mongo_collection = mongo_collection

    async def handling_message(self, message):
        """Метод в обработки сообщений"""
        message_to_send = await self.prepare_message_to_send(message=message)
        if not message_to_send:
            logger.error(f"The queue {self.task_queue} is missing in rabbitmq")
        else:
            await self.sender.send(message=message_to_send)
            await self.mongo.add_document(
                collection=self.mongo_collection, document=message_to_send
            )

    async def prepare_message_to_send(self, message):
        """Метод подготовки сообщения для отправки"""
        try:
            message_to_send = ""
            if self.task_queue == os.getenv(
                "REGISTRATION_EVENT_QUEUE", "registration_event:queue"
            ):
                message = models.RegistrationEmailModel(
                    firstname=message.get("firstname"), email=message.get("email")
                )
                message_to_send = models.EmailData(
                    email=message.email,
                    subject=message.subject,
                    text=f"Dear {message.firstname}, thank you for registering on our online movie theater",
                )
            elif self.task_queue == os.getenv(
                "ADMINISTRATION_EVENT_QUEUE", "administration_event:queue"
            ):
                message = models.AdministrationEmail(
                    firstname=message.get("firstname"),
                    email=message.get("email"),
                    subject=message.get("subject"),
                    text=message.get("text"),
                )
                message_to_send = models.EmailData(
                    email=message.email, subject=message.subject, text=message.text
                )
            elif self.task_queue == os.getenv(
                "SCHEDULER_BOOKMARKS_Q", "scheduler_bookmarks_event:queue"
            ):
                message = models.SchedulerBookmarksEmail(
                    firstname=message["user"].get("first_name"),
                    email=message["user"].get("email"),
                    films=message.get("films"),
                )
                message_to_send = models.EmailData(
                    email=message.email,
                    subject=message.subject,
                    text=", ".join(message.films),
                )
            return message_to_send
        except ValidationError as err:
            logger.error(msg=err.json(), exc_info=True)

    async def work(self):
        """Метод собирает асинхронные задачи и запускает их"""
        tasks = []
        while message := await self.rabbit.consume_from_queue(queue=self.task_queue):
            logger.info(msg=f"Received message {message}")
            tasks.append(asyncio.create_task(self.handling_message(message=message)))
        await asyncio.gather(*tasks)
