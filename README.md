# oeliks-server
better clone version of OLX online market platform

## Setting up with docker
- install docker engine
- clone the repository
- `docker compose up --build`

## Setting up manually

- install python and docker
- `pip install poetry`
- `poetry install`
- set up `.env` file

### Running the server

- `sudo docker run -d -p 6379:6379 redis:6.2-alpine`
- `sudo docker run -e MYSQL_ROOT_PASSWORD=pwd -d -p 3306:3306 mysql`
- `poetry run celery -A core worker --loglevel=info` (add `-P solo` in windows)
- `poetry run celery -A core beat`
- `poetry run celery -A core flower`
- `poetry run python manage.py runserver`

## Other commands

- to stop running tasks in celery
  `celery -A core purge`
  or
  `from core.celery import app`
  `app.control.purge()`
