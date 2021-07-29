from os import getenv

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from jobs import jobs_list

scheduler_thread_pool = int(getenv("SCHEDULER_THREAD_POOL"))
postgres_dsn = getenv("POSTGRES_DSN")
scheduler_max_instances = getenv("SCHEDULER_MAX_INSTANCES")


class Config:
    JOBS = jobs_list

    SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url=postgres_dsn)}

    SCHEDULER_EXECUTORS = {
        "default": {"type": "threadpool", "max_workers": scheduler_thread_pool}
    }

    SCHEDULER_JOB_DEFAULTS = {
        "coalesce": False,
        "max_instances": scheduler_max_instances,
    }

    SCHEDULER_API_ENABLED = True
