#!/bin/sh
set -e

echo "Waiting for MinIO to be ready..."
until mc alias set minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD} > /dev/null 2>&1; do
  echo "MinIO is not ready yet. Waiting..."
  sleep 2
done

echo "MinIO is ready. Setting up bucket and policies..."

# Create bucket if it doesn't exist
mc mb minio/${MINIO_BUCKET} --ignore-existing || true

# Set bucket policy to public read
mc anonymous set public minio/${MINIO_BUCKET} || true

# Set CORS policy using mc command
if [ -f /tmp/cors.json ]; then
    mc cors set /tmp/cors.json minio/${MINIO_BUCKET} || true
else
    echo "CORS config file not found, skipping CORS setup"
fi

echo "MinIO initialization completed successfully!"
