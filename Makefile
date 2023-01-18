dev:
	pipenv run python -m app

install:
	pipenv install

test:
	pipenv run pytest -vvv app

build:
	docker build \
		--tag docker.coma-dev.ru/social-network/api:$V \
		--tag docker.coma-dev.ru/social-network/api:latest \
		--file templates/Dockerfile \
		.
