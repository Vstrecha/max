#!/bin/bash

# Use environment variables with defaults
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 0.1
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application
echo "Starting max-events application..."
exec gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
