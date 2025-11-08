#!/bin/bash
set -e

echo "Waiting for database to be ready..."
while ! python -c "import psycopg2; psycopg2.connect(dbname='${DB_NAME}', user='${DB_USER}', password='${DB_PASSWORD}', host='${DB_HOST}', port='${DB_PORT}')" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 1
done

echo "Database is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python create_superuser.py

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8001
