# Backend Service

FastAPI backend сервис для системы управления мероприятиями.

## Описание

Backend сервис предоставляет REST API для работы с профилями пользователей, мероприятиями, друзьями и файлами. Использует PostgreSQL для хранения данных и MinIO для хранения файлов.

## Технологии

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - миграции базы данных
- **PostgreSQL** - реляционная база данных
- **MinIO** - S3-совместимое хранилище файлов
- **Pydantic** - валидация данных

## API Endpoints

### Профили
- `GET /v1/profiles/` - получить список профилей
- `GET /v1/profiles/me` - получить текущий профиль
- `PATCH /v1/profiles/me` - обновить текущий профиль

### Мероприятия
- `GET /v1/global_events/` - получить список мероприятий
- `GET /v1/global_events/{event_id}` - получить детали мероприятия
- `POST /v1/global_events/` - создать мероприятие
- `PATCH /v1/global_events/{event_id}` - обновить мероприятие
- `DELETE /v1/global_events/{event_id}` - удалить мероприятие
- `POST /v1/user_events/{event_id}` - зарегистрироваться на мероприятие
- `DELETE /v1/user_events/{event_id}` - отменить регистрацию

### Друзья
- `GET /v1/friends/` - получить список друзей
- `POST /v1/friends/{friend_id}` - добавить друга
- `DELETE /v1/friends/{friend_id}` - удалить друга

### Файлы
- `POST /v1/files/upload` - загрузить файл
- `GET /v1/files/` - получить список файлов
- `GET /v1/files/{file_id}` - получить файл
- `DELETE /v1/files/{file_id}` - удалить файл

## Аутентификация

Все API endpoints требуют Max Mini App авторизацию через заголовок `Authorization`:

```
Authorization: tma <init_data>
```

## Запуск

### Через Docker Compose

```bash
docker-compose up backend
```

### Локально

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Переменные окружения

- `DB_HOST` - хост базы данных
- `DB_NAME` - имя базы данных
- `DB_USER` - пользователь базы данных
- `DB_PASSWORD` - пароль базы данных
- `BOT_TOKEN` - токен Max бота
- `S3_ACCESS_KEY` - ключ доступа к S3
- `S3_SECRET_KEY` - секретный ключ S3
- `S3_BUCKET` - имя bucket в S3
- `S3_ENDPOINT_URL` - URL endpoint S3
- `S3_PUBLIC_URL` - публичный URL для доступа к файлам
- `S3_REGION` - регион S3

## Миграции базы данных

Миграции применяются автоматически при запуске сервиса.

Для ручного применения:

```bash
docker-compose exec backend alembic upgrade head
```

Создание новой миграции:

```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## Тестирование

```bash
docker-compose exec backend pytest
```

## Документация API

После запуска сервиса документация доступна по адресу:
- Swagger UI: `https://your-domain.com/docs`
- ReDoc: `https://your-domain.com/redoc`
