# Format code
.PHONY: fmt
fmt:
	black .
	isort .

# Copy env file
copy_env_file:
	cp .env.sample .env

up:
	docker-compose up -d --build

down:
	docker-compose down --remove-orphans

down-clear:
	docker-compose down -v --remove-orphans


		init: copy_env_file up create_schema_and_populate_from_sqlite django-migrate \
		es_create_schema es_transfer_from_postgres_pipline_start

create_schema_and_populate_from_sqlite:
	docker-compose run --rm etl-cli python es_pgsql_initial_population/move_from_sqlite/load_data.py

django-migrate:
	docker-compose exec django ./manage.py migrate --fake movies 0001
	docker-compose exec django ./manage.py migrate

django-create-superuser:
	docker-compose exec django ./manage.py createsuperuser

django-collectstatic:
	docker-compose exec django ./manage.py collectstatic --noinput


es_create_schema:
	 docker-compose run --rm etl-cli python es_pgsql_initial_population/create_schema.py

es_transfer_from_postgres_pipline_start:
	docker-compose run --rm etl-cli python main.py
