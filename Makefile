include .env

COMPOSE_FILE := dev-mac.compose.yml

ifeq ($(APP_ENV),production)
COMPOSE_FILE := prod-compose.yml
endif

DOCKERCOMPOSE := docker-compose -f $(COMPOSE_FILE)

.PHONY: run-tunnel dev-exec-app

## Запустить SSH туннель для webhook
run-tunnel:
	@docker run --net=host -it pinggy/pinggy -p 443 -R0:localhost:$(APP_PORT) -L4300:localhost:4300 a.pinggy.io

## Зайти в контейнер с FastAPI
dev-exec-app:
	$(DOCKERCOMPOSE) exec app bash

