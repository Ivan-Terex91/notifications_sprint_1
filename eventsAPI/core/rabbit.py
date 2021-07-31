from typing import Optional

from aio_pika import RobustConnection

rabbit_connection: Optional[RobustConnection] = None


async def get_rabbit_connection() -> Optional[RobustConnection]:
    return rabbit_connection
