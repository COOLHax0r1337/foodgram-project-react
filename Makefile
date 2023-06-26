build_statics:
	docker compose exec backend python manage.py collectstatic
	docker compose exec backend cp -r /app/collected_static/. /static/static/

migrate: build_statics
	docker compose exec backend python manage.py migrate

superuser:
	docker compose exec backend python manage.py createsuperuser

run_docker:
	docker compose up -d