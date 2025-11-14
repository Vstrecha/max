# Встреча - Система управления мероприятиями

Docker-образ для запуска полнофункциональной системы управления мероприятиями с поддержкой Max Mini App.

## Быстрый старт

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл и укажите необходимые значения.

### 2. Запуск проекта

#### Сборка и запуск всех сервисов:

```bash
docker-compose up -d --build
```

#### Просмотр логов:

```bash
docker-compose logs -f
```

#### Остановка сервисов:

```bash
docker-compose down
```

### 3. Примеры команд

```bash
# Просмотр статуса контейнеров
docker-compose ps

# Просмотр логов конкретного сервиса
docker-compose logs -f backend

# Перезапуск сервиса
docker-compose restart backend

# Остановка всех сервисов
docker-compose down

# Остановка с удалением volumes (ОСТОРОЖНО: удалит данные!)
docker-compose down -v
```

## Доступ к сервисам

После запуска сервисы будут доступны по следующим адресам:

- **Frontend**: `https://your-domain.com/`
- **Backend API**: `https://your-domain.com/api/`
- **API Документация**: `https://your-domain.com/docs`
- **Admin панель**: `https://your-domain.com/admin/`

## Первоначальная настройка

### Создание суперпользователя в admin панели

```bash
docker-compose exec admin python manage.py createsuperuser
```

## Зависимости

Все зависимости описаны в файле `requirements.txt` в корне проекта.

## Поддержка

При возникновении проблем проверьте логи:

```bash
docker-compose logs
```

Или логи конкретного сервиса:

```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs admin
docker-compose logs nginx
docker-compose logs minio
```
