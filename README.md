# Max Events - Система управления мероприятиями

Система управления мероприятиями с поддержкой Max Mini App. Доступна как Docker-образ на GitHub Container Registry.

## 🚀 Быстрый старт с Docker-образом

### Вариант 1: Использование готового образа из GitHub Container Registry

#### 1. Получение образа

```bash
docker pull ghcr.io/<ваш-username>/<название-репозитория>:latest
```

Или используйте конкретную версию:

```bash
docker pull ghcr.io/<ваш-username>/<название-репозитория>:v1.0.0
```

#### 2. Настройка переменных окружения

Создайте файл `.env` со следующими переменными:

```bash
# База данных PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_NAME=max_events
DB_USER=postgres
DB_PASSWORD=your_password

# MinIO (S3-совместимое хранилище)
MINIO_HOST=minio
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET=files

# Nginx
NGINX_HOST=localhost

# Backend настройки
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Admin настройки
ADMIN_HOST=0.0.0.0
ADMIN_PORT=8001
```

#### 3. Запуск с Docker Compose (рекомендуется)

Создайте файл `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:17
    container_name: max-events-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  minio:
    image: minio/minio:latest
    container_name: max-events-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  app:
    image: ghcr.io/<ваш-username>/<название-репозитория>:latest
    container_name: max-events-app
    restart: unless-stopped
    env_file:
      - .env
    environment:
      DB_HOST: db
      MINIO_HOST: minio
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - db
      - minio
    volumes:
      - ./logs:/var/log

volumes:
  postgres_data:
  minio_data:
```

Запуск:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### 4. Запуск отдельного контейнера

```bash
docker run -d \
  --name max-events-app \
  --env-file .env \
  -e DB_HOST=your-db-host \
  -e MINIO_HOST=your-minio-host \
  -p 80:80 \
  -p 443:443 \
  ghcr.io/<ваш-username>/<название-репозитория>:latest
```

### Вариант 2: Локальная сборка и запуск

#### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd max
```

#### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта (см. пример выше).

#### 3. Сборка образа

```bash
docker build -t max-events:latest \
  --build-arg VITE_HOST_API_URL=http://localhost/api \
  .
```

#### 4. Запуск с Docker Compose

```bash
docker-compose up -d --build
```

## 📦 Сборка и публикация образа

### Автоматическая публикация

При пуше в ветку `main` или создании тега GitHub Actions автоматически собирает и публикует образ в GitHub Container Registry.

### Ручная публикация

```bash
# Вход в GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Сборка образа
docker build -t ghcr.io/USERNAME/REPO:latest \
  --build-arg VITE_HOST_API_URL=https://your-domain.com/api \
  .

# Публикация образа
docker push ghcr.io/USERNAME/REPO:latest
```

## 🌐 Доступ к сервисам

После запуска сервисы будут доступны по следующим адресам:

- **Frontend**: `http://localhost/` или `https://your-domain.com/`
- **Backend API**: `http://localhost/api/` или `https://your-domain.com/api/`
- **API Документация**: `http://localhost/docs` или `https://your-domain.com/docs`
- **Admin панель**: `http://localhost/admin/` или `https://your-domain.com/admin/`
- **MinIO Console**: `http://localhost:9001` (если проброшен порт)

## ⚙️ Первоначальная настройка

### Создание суперпользователя в admin панели

```bash
docker exec -it max-events-app python /app/admin/manage.py createsuperuser
```

Или через скрипт:

```bash
docker exec -it max-events-app python /app/admin/create_superuser.py
```

## 📋 Управление контейнером

```bash
# Просмотр логов
docker logs -f max-events-app

# Просмотр статуса
docker ps | grep max-events

# Перезапуск
docker restart max-events-app

# Остановка
docker stop max-events-app

# Удаление
docker rm max-events-app
```

## 🔧 Переменные окружения

### Обязательные переменные

- `DB_HOST` - хост базы данных PostgreSQL
- `DB_PORT` - порт базы данных (по умолчанию: 5432)
- `DB_NAME` - имя базы данных
- `DB_USER` - пользователь базы данных
- `DB_PASSWORD` - пароль базы данных
- `MINIO_HOST` - хост MinIO сервера
- `MINIO_PORT` - порт MinIO (по умолчанию: 9000)
- `NGINX_HOST` - доменное имя для Nginx

### Опциональные переменные

- `MINIO_ROOT_USER` - пользователь MinIO (по умолчанию: minioadmin)
- `MINIO_ROOT_PASSWORD` - пароль MinIO (по умолчанию: minioadmin)
- `MINIO_BUCKET` - имя bucket в MinIO (по умолчанию: files)
- `MINIO_CONSOLE_PORT` - порт MinIO Console (по умолчанию: 9001)

## 🐛 Решение проблем

### Просмотр логов

```bash
# Все логи
docker logs max-events-app

# Логи конкретного сервиса (через supervisor)
docker exec max-events-app tail -f /var/log/backend.out.log
docker exec max-events-app tail -f /var/log/admin.out.log
docker exec max-events-app tail -f /var/log/nginx.out.log
```

### Проверка подключения к БД

```bash
docker exec max-events-app nc -z ${DB_HOST} ${DB_PORT}
```

### Проверка здоровья контейнера

```bash
docker inspect max-events-app | grep Health -A 10
```

## 📚 Дополнительная информация

- Все зависимости описаны в файлах `requirements.txt` в соответствующих директориях
- Frontend собирается во время создания образа с использованием переменной `VITE_HOST_API_URL`
- Backend и Admin автоматически выполняют миграции при запуске
- Supervisor управляет процессами backend, admin и nginx внутри контейнера
