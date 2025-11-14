# Multi-stage build для Max Events приложения

# Stage 1: Frontend build
FROM node:25-alpine AS frontend-builder
WORKDIR /app/frontend
ARG VITE_HOST_API_URL
ENV VITE_HOST_API_URL=${VITE_HOST_API_URL}
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Backend dependencies
FROM python:3.12-slim AS backend-deps
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Stage 3: Admin dependencies
FROM python:3.12-slim AS admin-deps
WORKDIR /app/admin
COPY admin/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 4: Final image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    netcat-traditional \
    postgresql-client \
    curl \
    dos2unix \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY --from=backend-deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=backend-deps /usr/local/bin /usr/local/bin
COPY backend/ /app/backend/
RUN chmod +x /app/backend/start.sh && dos2unix /app/backend/start.sh

# Copy admin
COPY --from=admin-deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY admin/ /app/admin/
RUN chmod +x /app/admin/start.sh && dos2unix /app/admin/start.sh

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx config template for Docker
COPY nginx/default.conf.docker /etc/nginx/templates/default.conf.template

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create entrypoint script for environment variable substitution
RUN echo '#!/bin/bash\n\
set -e\n\
envsubst "$$NGINX_HOST $$MINIO_HOST $$MINIO_PORT $$MINIO_CONSOLE_PORT" < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf\n\
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Create necessary directories
RUN mkdir -p /app/backend/uploads /var/log

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV NGINX_HOST=localhost
ENV MINIO_HOST=minio
ENV MINIO_PORT=9000
ENV MINIO_CONSOLE_PORT=9001

# Expose ports
EXPOSE 80 443 8000 8001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start via entrypoint
ENTRYPOINT ["/entrypoint.sh"]
