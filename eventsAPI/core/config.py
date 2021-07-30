import os

PROJECT_NAME = "eventsAPI"
RABBIT_DSN = os.getenv("RABBIT_DSN", "amqp://guest:guest@localhost:5672/")
