import os

from aio_pika import DeliveryMode, Message


async def publish_bookmarks_event(connection, event):
    async with connection.channel() as channel:
        message = Message(
            body=event.encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(
            message,
            routing_key=os.getenv(
                "SCHEDULER_BOOKMARKS_Q", "scheduler_bookmarks_event:queue"
            ),
        )
