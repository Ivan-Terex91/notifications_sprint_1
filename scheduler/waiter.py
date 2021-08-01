import asyncio
import logging

import aio_pika
import config

logger = logging.getLogger(__name__)


async def waiter_rabbit():
    """Waiter для rabbitmq"""
    rabbit_status = 0
    while not rabbit_status:
        try:
            connection = await aio_pika.connect_robust(url=config.rabbit_dsn)
            await connection.close()
            rabbit_status = 1
        except ConnectionError as exc:
            logger.error(exc)
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(waiter_rabbit())
