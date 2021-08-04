import sentry_sdk
import uvicorn
from api.v1 import bookmark, rating, review
from core import auth, config, mongo  # type: ignore
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    auth.auth_client = auth.AuthClient(base_url=config.AUTH_URL)
    mongo.mongo_client = AsyncIOMotorClient(config.MONGO_DSN)


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_client.close()


app.include_router(rating.router, prefix="/api/v1/rating", tags=["ratings"])
app.include_router(review.router, prefix="/api/v1/review", tags=["reviews"])
app.include_router(bookmark.router, prefix="/api/v1/bookmark", tags=["bookmarks"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7777, reload=True)
