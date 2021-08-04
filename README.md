# Проектная работа 10 спринта

# Запуск проекта
1. Скопировать переменные окружения командой `make copy_env_file`.
2. Запустить `docker-compose up -d --build`
3. Запустить `make init`
4. Собрать статику для `Administration event service` командой `docker-compose exec administration python manage.py 
   collectstatic`
5. Для поднятия базы и коллекций в MongoDB сервиса `UGC` выполнить команду `bash up_mongo.sh`
6. Для поднятия базы и коллекций в MongoDB сервиса `Notifications` выполнить команду `bash events_collections.sh`

# UGC_API
Swagger - `http://127.0.0.1:7777/api/openapi`

# EventsAPI
Swagger - `http://127.0.0.1:10000/api/openapi`

# Auth
Swagger - `http://127.0.0.1:8001/`

# Administration event service
`http://127.0.0.1:8000/admin/`

Команда создания суперпользователя `docker-compose exec administration python manage.py createsuperuser` 


# Scheduler API

* /scheduler [GET] > returns basic information about the app
* /scheduler/jobs [POST json job data] > adds a job to the scheduler
* /scheduler/jobs/<job_id> [GET] > returns json of job details
* /scheduler/jobs [GET] > returns json with details of all jobs
* /scheduler/jobs/<job_id> [DELETE] > deletes job from scheduler
* /scheduler/jobs/<job_id> [PATCH json job data] > updates an already existing job
* /scheduler/jobs/<job_id>/pause [POST] > pauses a job, returns json of job details
* /scheduler/jobs/<job_id>/resume [POST] > resumes a job, returns json of job details
* /scheduler/jobs/<job_id>/run [POST] > runs a job now, returns json of job details

# Задачи спринта

[CI/CD](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/3)
1. Был добавлен функционал CI/CD согласно заданию к спринту

[UML](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/4)
1. Была добавлена UML диаграмма
P.S. В процессе разработки диаграмма была немного подправлена в [коммите](https://github.com/Ivan-Terex91/notifications_sprint_1/commit/c55fba118f8be357289c3aa3489d0f068ff50b60)

[API для приёма событий](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/11)
1. Были реализованы Api методы и views для приёма событий
2. Продюссеры для отправки сообщений в очереди rabbitmq

[Отправка событий о регистрации пользователя в API](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/12)
1. Была реализована отправка событий о регистрации пользователя
P.S. В процессе разработки была добалена отдельная модель в auth в этом [коммите](https://github.com/Ivan-Terex91/notifications_sprint_1/commit/be6f76b22d958a58b6b0b294b1d54f31fd2d2e1c)

[Сервис отправки писем администраторами](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/14)
1. Была реализована административная панель на джанго и добавлен простой action для отправки уведомлений

[Планировщик задач](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/13)
1. Был реализован планировщик задач
2. Продюссер для отправки событий в очередь rabbitmq

[Сервис обработки очередей (consumers/workers)](https://github.com/Ivan-Terex91/notifications_sprint_1/pull/16)
1. Были реализованы консумеры под каждую очередь rabbitmq
2. Рассылка уведомлений по email