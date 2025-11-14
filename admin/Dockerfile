FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install dos2unix for line ending conversion and make start script executable
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix start.sh && \
    chmod +x start.sh && \
    rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 8001

# Run start script which handles migrations and superuser creation
CMD ["/bin/bash", "/app/start.sh"]
