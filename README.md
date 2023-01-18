# Solution for the technical task

[Made by coma8675](https://github.com/coma8765-dev)

## Stack:

### Technologies: 
* python3.11
* pipenv
* FastAPI
* AsyncPG
* Postgres

### Architecture: 
* DDD - domain driven design
* TDD - test driven development

## Run it

### Via Docker Compose
```shell
docker compose --file templates/docker-compose.yaml up api-pg -d
docker compose --file templates/docker-compose.yaml up api -d
```
_App will start at [http://localhost:8000/docs](http://localhost:8000/docs)_


### Bare

#### Install dependencies

```shell
pip install pipenv 
pipenv install
```

#### Setup database
You need make copy `.env.example` with some params for connect to postgres database

#### Run application

```shell
pipenv run python -m app  # Alternative: "make dev"
```

## Test it
### Via docker compose
```shell
docker compose --file templates/docker-compose.yaml exec -it api python -m pytest app
```

### Bare
```shell
pipenv run python -m pytest app  # Alternative: "make test"
```
