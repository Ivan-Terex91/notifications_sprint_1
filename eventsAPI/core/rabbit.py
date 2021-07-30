from aio_pika import RobustConnection

rabbit_connection: RobustConnection = None


async def get_rabbit_connection() -> RobustConnection:
    return rabbit_connection
