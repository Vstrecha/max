#!/bin/bash
set -e

cd "$HOME/max"

echo "🔄 Pulling latest code"
git reset --hard origin/main && git pull

echo "🚀 Starting services"
docker compose down --remove-orphans
# docker volume rm max_frontend-dist
docker compose up --build -d
