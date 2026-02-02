include .env

PYTHON_DEV_IMAGE=python:3.11
DOCKERCOMPOSE=docker-compose -f dev-mac.compose.yml

.PHONY: run-tunnel dev-exec-app dev-start

## Запустить SSH туннель для webhook
run-tunnel:
	@docker run --net=host -it pinggy/pinggy -p 443 -R0:localhost:$(APP_PORT) -L4300:localhost:4300 a.pinggy.io

## Зайти в контейнер с FastAPI
dev-exec-app:
	$(DOCKERCOMPOSE) exec app bash

# Запустить проект
dev-start:
    $(DOCKERCOMPOSE) PYTHON_DEV_IMAGE=$(PYTHON_DEV_IMAGE) --force-recreate --build

dev-build-app:
    @docker build -t $(PYTHON_DEV_IMAGE) -f docker/python/Dockerfile docker/images