# Проектная работа 10 спринта

# Запуск проекта
1. Скопировать переменные окружения командой `make copy_env_file`.
2. Запустить `docker-compose up -d --build`
3. Собрать статику для `Administration event service` командой `docker-compose exec administration python manage.py 
   collectstatic`


# EventsAPI
Swagger - `http://127.0.0.1:10000/api/openapi`

# Auth
Swagger - `http://127.0.0.1:8001/`

# Administration event service
`http://127.0.0.1:8000/admin/`

Команда создания суперпользователя `docker-compose exec administration python manage.py createsuperuser` 


# Scheduler API

/scheduler [GET] > returns basic information about the app
/scheduler/jobs [POST json job data] > adds a job to the scheduler
/scheduler/jobs/<job_id> [GET] > returns json of job details
/scheduler/jobs [GET] > returns json with details of all jobs
/scheduler/jobs/<job_id> [DELETE] > deletes job from scheduler
/scheduler/jobs/<job_id> [PATCH json job data] > updates an already existing job
/scheduler/jobs/<job_id>/pause [POST] > pauses a job, returns json of job details
/scheduler/jobs/<job_id>/resume [POST] > resumes a job, returns json of job details
/scheduler/jobs/<job_id>/run [POST] > runs a job now, returns json of job details
