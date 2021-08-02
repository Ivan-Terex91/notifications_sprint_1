jobs_list = [
    {
        "id": "job1",
        "func": "job_definitions:new_films_of_week",
        "replace_existing": True,
        "args": (1, 2),
        "trigger": "cron",
        "day_of_week": "fri",
        "hour": 18,
    },
    {
        "id": "job2",
        "func": "job_definitions:saved_films",
        "replace_existing": True,
        "trigger": "cron",
        "day": "1st sat",
        "hour": 18,
    },
    {
        "id": "test_job",
        "func": "job_definitions:saved_films",
        "replace_existing": True,
        "trigger": "interval",
        "seconds": 5,
    },
]
