from motor.motor_asyncio import AsyncIOMotorClient


class MongoService:
    """Класс для работы с mongo"""

    def __init__(self, mongo_client: AsyncIOMotorClient, db: str):
        self.mongo_client = mongo_client
        self.db = db

    async def add_document(self, collection: str, document):
        """Метод добавления документа в коллекцию"""
        await self.mongo_client[self.db][collection].insert_one(document.dict())
