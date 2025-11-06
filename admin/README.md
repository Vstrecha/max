# Django Admin Panel

Админ-панель для управления пользователями и мероприятиями.

## Установка и запуск

### Через Docker Compose

```bash
docker-compose up admin
```

### Создание суперпользователя

```bash
# Через Docker
docker-compose exec admin python create_superuser.py

# Или вручную
docker-compose exec admin python manage.py createsuperuser
```

## Доступ

- URL: http://localhost:8001/admin/
- Логин: admin (или созданный суперпользователь)
- Пароль: admin123 (или установленный пароль)

## Функциональность

### Пользователи (Profiles)
- Список всех пользователей
- История регистраций на мероприятия
- Количество посещенных мероприятий
- Детальная информация о каждом пользователе

### Мероприятия (Events)
- Список всех мероприятий
- Статистика регистраций
- Статистика посещений
- Процент посещаемости
- Список участников с отметкой о посещении

### Участия (Event Participations)
- Список всех регистраций
- Статус посещения (пришел/не пришел)

### QR Сканирования (QR Scans)
- История всех сканирований QR-кодов
- Информация о том, кто и когда сканировал

## Переменные окружения

Админка использует те же переменные окружения, что и backend:
- `POSTGRES_DB` или `DB_NAME` - имя базы данных
- `POSTGRES_USER` или `DB_USER` - пользователь БД
- `POSTGRES_PASSWORD` или `DB_PASSWORD` - пароль БД
- `POSTGRES_HOST` или `DB_HOST` - хост БД (по умолчанию `db`)
- `POSTGRES_PORT` или `DB_PORT` - порт БД (по умолчанию `5432`)

Для создания суперпользователя:
- `DJANGO_SUPERUSER_USERNAME` - имя пользователя (по умолчанию `admin`)
- `DJANGO_SUPERUSER_EMAIL` - email (по умолчанию `admin@example.com`)
- `DJANGO_SUPERUSER_PASSWORD` - пароль (по умолчанию `admin123`)
