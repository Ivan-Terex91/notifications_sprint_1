import os

PROJECT_NAME = "User generated content"
MONGO_DSN = os.getenv("MONGO_DSN", "mongodb://localhost:27017")
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001/")
DB = os.getenv("DB", "ugcDb")
RATING_COLLECTION = os.getenv("RATING_COLLECTION", "movie_ratingCollection")
REVIEW_COLLECTION = os.getenv("REVIEW_COLLECTION", "movie_reviewCollection")
BOOKMARK_COLLECTION = os.getenv("BOOKMARK_COLLECTION", "movie_bookmarkCollection")
SENTRY_DSN = os.getenv("SENTRY_DSN", "None")
