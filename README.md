# Проектная работа 10 спринта

Проектные работы в этом модуле выполняются в одиночку, без деления на команды. Задания на спринт вы найдёте внутри тем.

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
