import json
import logging
import os

import aio_pika
from aio_pika import DeliveryMode, Message, RobustConnection
import uvicorn as uvicorn
from core import config, rabbit
from core.logger import LOGGING
from core.rabbit import get_rabbit_connection
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from models.administration_event import AdministrationEventModel
from models.rating_review_event import RatingReviewEventModel
from models.registration_user_event import RegistrationUserEventModel

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    rabbit.rabbit_connection = await aio_pika.connect_robust(url=config.RABBIT_DSN)


@app.on_event("shutdown")
async def shutdown():
    await rabbit.rabbit_connection.close()


@app.post("/administration_event/", tags=["events"])
async def add_administration_event(
    administration_event: AdministrationEventModel,
    rabbit_connection: RobustConnection = Depends(get_rabbit_connection),
):
    """Событие от администраторов"""
    async with rabbit_connection.channel() as channel:
        message = Message(
            body=json.dumps(administration_event.dict(), default=str).encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(
            message,
            routing_key=os.getenv(
                "ADMINISTRATION_EVENT_QUEUE", "administration_event:queue"
            ),
        )


@app.post("/rating_review_event/", tags=["events"])
async def add_rating_review_event(
    rating_review_event: RatingReviewEventModel,
    rabbit_connection: RobustConnection = Depends(get_rabbit_connection),
):
    """Событие о оценке ревью"""
    async with rabbit_connection.channel() as channel:
        message = Message(
            body=json.dumps(rating_review_event.dict(), default=str).encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(
            message,
            routing_key=os.getenv(
                "RATING_REVIEW_EVENT_QUEUE", "rating_review_event:queue"
            ),
        )


@app.post("/registration_user_event/", tags=["events"])
async def add_registration_user_event(
    registration_event: RegistrationUserEventModel,
    rabbit_connection: RobustConnection = Depends(get_rabbit_connection),
):
    """Событие о регистрации пользователя"""
    async with rabbit_connection.channel() as channel:
        message = Message(
            body=json.dumps(registration_event.dict(), default=str).encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await channel.default_exchange.publish(
            message,
            routing_key=os.getenv(
                "REGISTRATION_EVENT_QUEUE", "registration_event:queue"
            ),
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
