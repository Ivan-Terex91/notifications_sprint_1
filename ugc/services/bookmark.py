from core import config
from core.mongo import get_mongo_client
from fastapi import Depends
from models.bookmark import MovieBookmark
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import UUID4


class BookmarkService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.collection = self.mongo_client[config.DB][config.BOOKMARK_COLLECTION]

    async def add_bookmark(self, movie_id: UUID4, user_id: UUID4):
        if await self.collection.find_one({"movie_id": movie_id, "user_id": user_id}):
            return False
        await self.collection.insert_one(
            MovieBookmark(user_id=user_id, movie_id=movie_id).dict()
        )
        return True

    async def delete_bookmark(self, movie_id: UUID4, user_id: UUID4):
        deleted = await self.collection.delete_one(
            {"user_id": user_id, "movie_id": movie_id}
        )
        return deleted.deleted_count

    async def get_list_bookmark(self, user_id: UUID4):
        movie_bookmarks = []
        bookmarks = self.collection.find({"user_id": user_id})
        async for bookmark in bookmarks:
            bookmark["_id"] = str(bookmark["_id"])
            movie_bookmarks.append(bookmark)
        return movie_bookmarks


def get_bookmark_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> BookmarkService:
    return BookmarkService(mongo_client=mongo_client)
