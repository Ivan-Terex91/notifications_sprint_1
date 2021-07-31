import logging
from enum import Enum

from flask import request


def extend_enum(inherited_enum):
    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True
