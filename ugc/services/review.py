from api.v1.models.review import ReviewModel as ReviewModelIn
from bson import ObjectId
from core import config
from core.mongo import get_mongo_client
from fastapi import Depends
from models.review import ReviewModel
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import UUID4


class ReviewService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.collection = self.mongo_client[config.DB][config.REVIEW_COLLECTION]

    async def add_review(
        self, movie_id: UUID4, user_id: UUID4, text: str, rating: float
    ):
        if await self.collection.find_one({"movie_id": movie_id, "user_id": user_id}):
            return False
        movie_review = ReviewModelIn(
            movie_id=movie_id, user_id=user_id, text=text, rating=rating
        )
        await self.collection.insert_one(movie_review.dict())
        return True

    async def add_or_update_review_rating(
        self, review_id: str, user_id: UUID4, rating: float
    ):
        if not await self.collection.find_one({"_id": ObjectId(review_id)}):
            return False
        if await self.collection.find_one(
            {"_id": ObjectId(review_id), "user_rating_review.user_id": user_id}
        ):
            await self.collection.update_one(
                {"_id": ObjectId(review_id), "user_rating_review.user_id": user_id},
                {"$set": {"user_rating_review.$.rating": rating}},
            )

        else:
            await self.collection.update_one(
                {"_id": ObjectId(review_id)},
                {
                    "$push": {
                        "user_rating_review": {"user_id": user_id, "rating": rating}
                    }
                },
            )
        return True

    async def get_film_reviews(self, movie_id: UUID4, sort_value: str, sort_order: int):

        reviews = []
        reviews_sort = self.collection.aggregate(
            [{"$match": {"movie_id": movie_id}}, {"$sort": {sort_value: sort_order}}]
        )

        async for review in reviews_sort:
            reviews.append(ReviewModel(id=str(review["_id"]), **review).dict())
        return reviews


def get_review_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> ReviewService:
    return ReviewService(mongo_client=mongo_client)
