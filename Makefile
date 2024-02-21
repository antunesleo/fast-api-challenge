help:
	@echo 'Available commands:'
	@echo ''
	@echo 'build ................................ Build docker image'
	@echo 'run .................................. Runs the webserver'
	@echo 'test ................................. Runs tests'
	@echo ''

build_base_image:
	docker build --tag=rafascar/fastapi-challenge --file=Dockerfile .

build:
	docker compose build

run:
	docker compose up

test:
	docker compose run --rm web pytest
