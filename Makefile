.PHONY: down
help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
down: ## stop docker container and remove orphans and volumes
	docker compose -f docker-compose.yaml down --volumes --remove-orphans
