import asyncio
import os
from typing import List

import aio_pika
import config


async def declare_queues(queues: List[str]):
    """Объявляем очереди до старта api"""
    connection = await aio_pika.connect_robust(url=config.RABBIT_DSN)
    async with connection.channel() as channel:
        for queue in queues:
            await channel.declare_queue(name=queue, durable=True)

    await connection.close()


if __name__ == "__main__":
    queues_list = (
        "administration_event:queue,registration_event:queue,rating_review_event:queue"
    )
    queues = os.getenv("ALL_QUEUES", queues_list).split(",")
    asyncio.run(declare_queues(queues=queues))
