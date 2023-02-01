.PHONY: down app exec-redis exec-app exec-postgres test test-logs
help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
down: ## stop docker container and remove orphans and volumes
	docker compose -f docker-compose.yaml down --volumes --remove-orphans
app: ## start main docker containers
	docker compose -f docker-compose.yaml up --build
exec-redis: ## execute redis container in bash > redis-cli
	docker exec -it hw_redis_cont bash -c 'redis-cli'
exec-app: ## execute app container in bash
	docker exec -it hw_app_cont bash
include .env
exec-postgres: ## execute postgres container in bash > psql
	docker exec -it hw_pgdb_cont bash -c 'psql -U $(POSTGRES_USER)'
test: ## start test docker containers
	docker compose -f docker-compose.test.yaml up --build
test-logs: ## show tests results
	docker logs hw_app_cont_test

