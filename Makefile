.PHONY: down stop exec-app exec-redis exec-postgres exec-rabbit up
help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
down: ## stop docker container and remove orphans and volumes
	docker compose -f docker-compose.yaml down --volumes --remove-orphans
up: ## start docker containers
	docker compose -f docker-compose.yaml up --build
stop: ## stop docker containers
	docker compose -f docker-compose.yaml stop
exec-app: ## execute app container in bash
	docker exec -it app bash
exec-redis: ## execute redis container in bash
	docker exec -it redis bash
include .env
exec-postgres: ## execute postgres container in bash > psql
	docker exec -it postgres bash -c 'psql -U $(POSTGRES_USER)'
exec-rabbit: ## execute rabbit container in bash
	docker exec -it rabbit bash
test: ##