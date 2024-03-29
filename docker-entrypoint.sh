#!/bin/bash

echo ">>> Waiting for MySQL to start..."
./wait-for-it.sh db:3306 -t 30

echo ">>> Preparing media directories"
mkdir media/ad
mkdir media/ad/images

echo ">>> Apply database migrations"
poetry run python manage.py migrate

echo ">>> Compile messages..."
poetry run python manage.py compilemessages > logs/compilemessages.log

echo ">>> Starting server..."
# poetry run python manage.py runserver 0.0.0.0:8000

if [ "$1" = "dev" ]; then
    echo ">> Running as developement server"
    # poetry run gunicorn --reload core.wsgi -w 3 -b 0.0.0.0:8000
    poetry run python manage.py runserver 0.0.0.0:8000
else
    echo ">> Collecting static files..."
    poetry run python manage.py collectstatic --noinput

    echo ">>> Populate database with dummy data"
    poetry run python manage.py createdata

    echo ">> Running as production server"
    poetry run gunicorn core.wsgi -w 3 -b 0.0.0.0:8000
fi