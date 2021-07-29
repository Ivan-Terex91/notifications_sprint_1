from core import config
from core.mongo import get_mongo_client
from fastapi import Depends
from models.rating import MovieRatingModel
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import UUID4


class RatingService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.collection = self.mongo_client[config.DB][config.RATING_COLLECTION]

    async def get_count_rating(self, movie_id):
        return await self.collection.count_documents({"movie_id": movie_id})

    async def get_avg_rating(self, movie_id):
        movie_agg = self.collection.aggregate(
            [
                {"$match": {"movie_id": movie_id}},
                {"$group": {"_id": movie_id, "avg_rating": {"$avg": "$rating"}}},
            ]
        )

        rating = []
        async for doc in movie_agg:
            rating.append(round(doc["avg_rating"], 2))

        return rating[0] if rating else rating

    async def add_rating(self, movie_id: UUID4, user_id: UUID4, rating: float):
        if await self.collection.find_one({"movie_id": movie_id, "user_id": user_id}):
            return False
        movie_rating = MovieRatingModel(
            movie_id=movie_id, user_id=user_id, rating=rating
        )
        await self.collection.insert_one(movie_rating.dict())
        return True

    async def change_rating(self, user_id: UUID4, movie_id: UUID4, rating: float):
        changed = await self.collection.update_one(
            {"user_id": user_id, "movie_id": movie_id}, {"$set": {"rating": rating}}
        )
        return changed.modified_count

    async def delete_rating(self, user_id: UUID4, movie_id: UUID4):
        deleted = await self.collection.delete_one(
            {"user_id": user_id, "movie_id": movie_id}
        )
        return deleted.deleted_count


def get_rating_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> RatingService:
    return RatingService(mongo_client=mongo_client)
