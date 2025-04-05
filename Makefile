.PHONY: init build run restart db-init db-migrate db-upgrade

init:  build run
	docker compose exec bank-service flask db init
	docker compose exec bank-service flask db migrate
	docker compose exec bank-service flask db upgrade
	docker compose exec bank-service flask init
	@echo "Init done, containers running"

build:
	docker compose build

run:
	docker compose up -d

rebuild:  down build run

down:
	docker compose down

db-init:
	docker compose exec bank-service flask db init

db-migrate:
	docker compose exec bank-service flask db migrate

db-upgrade:
	docker compose exec bank-service flask db upgrade
