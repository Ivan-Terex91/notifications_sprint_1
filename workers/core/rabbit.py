import json

from aio_pika import RobustConnection


class RabbitService:
    """Класс для работы с rabbitmq."""

    def __init__(self, connection: RobustConnection):
        self.connection = connection

    async def consume_from_queue(self, queue: str):
        """Метод для получения сообщений из очереди"""
        async with self.connection.channel() as channel:
            await channel.set_qos(prefetch_count=100)
            queue = await channel.declare_queue(name=queue, durable=True)
            async with queue.iterator() as queue_iter:  # type: ignore
                async for message in queue_iter:
                    async with message.process():
                        return json.loads(message.body)
