from os import getenv

admin_event_q = getenv("ADMINISTRATION_EVENT_QUEUE")
registration_event_q = getenv("REGISTRATION_EVENT_QUEUE")
rating_event_q = getenv("RATING_REVIEW_EVENT_QUEUE")
scheduler_bookmarks_q = getenv("SCHEDULER_BOOKMARKS_Q", "scheduler_bookmarks_event:queue")
rabbit_dsn = getenv("RABBIT_DSN")
queue_list = ",".join(["administration_event:queue",
                       "registration_event:queue",
                       "rating_review_event:queue",
                       "scheduler_bookmarks_event:queue"])
queues = getenv("ALL_QUEUES", queue_list).split(",")
