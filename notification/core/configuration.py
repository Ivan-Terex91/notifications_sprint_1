import os

PROJECT_NAME = "Notification service"
RABBIT_DSN = os.getenv("RABBIT_DSN", "amqp://guest:guest@localhost:5672/")
MONGO_DSN = os.getenv("MONGO_DSN", "mongodb://localhost:27017")
NOTIFICATION_COLLECTION = os.getenv("NOTIFICATION_COLLECTION", "notification_collection")
