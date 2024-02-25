#!/bin/bash

echo ">>> Waiting for MySQL to start..."
./wait-for-it.sh db:3306

echo ">>> Apply database migrations"
poetry run python manage.py migrate

# echo ">>> Collecting static files..."
# poetry run python manage.py collectstatic

echo ">>> Starting server..."
# poetry run python manage.py runserver 0.0.0.0:8000

if [ "$1" = "dev" ]; then
    echo ">> Running as developement server"
    poetry run gunicorn --reload core.wsgi -b 0.0.0.0:8000
else
    echo ">> Running as production server"
    poetry run gunicorn core.wsgi -b 0.0.0.0:8000
fi