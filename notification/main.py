import asyncio
import json
import logging

import aio_pika
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sendgrid import Mail

from core import configuration, rabbit
from core.sender import Sendgrid
from models.bookmarks_event import BookmarksEvent

app = FastAPI(
    title=configuration.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    logger = logging.getLogger(__name__)
    email_sender = Sendgrid()


    async def main(loop, q_name):
        connection = await aio_pika.connect_robust(
            rabbit.rabbit_dsn, loop=loop
        )

        queue_name = q_name

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True, auto_delete=False)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        content = json.loads(message.body)
                        content_obj = BookmarksEvent.parse_obj(content)
                        print(content)
                        user = content_obj.user
                        email = Mail(
                            from_email="oguseynov@yandex.ru",
                            to_emails=user.email,
                            subject="Do not forget to watch saved films",
                            plain_text_content=str(content_obj.films)
                        )
                        email_sender.send(email)

                        if queue.name in message.body.decode():
                            break


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, rabbit.scheduler_bookmarks_q))
    loop.close()
