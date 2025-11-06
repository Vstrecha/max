# Vstrecha API

FastAPI приложение для Telegram Mini App с полной CRUD функциональностью.

## 🏗️ Архитектура проекта

### Структура папок
```
app/
├── api/v1/                    # API endpoints
│   ├── endpoints/            # Ручки для сущностей
│   └── docs/examples/        # Примеры для документации
├── core/                     # Основная логика
│   ├── config.py            # Конфигурация
│   ├── middleware.py        # Логирование запросов
│   ├── docs_auth.py         # Аутентификация документации
│   └── telegram_auth.py     # Telegram авторизация
├── db/                       # База данных
│   ├── models/              # SQLAlchemy модели
│   ├── crud/                # CRUD операции
│   └── session.py           # Сессии БД
├── schemas/                  # Pydantic схемы
└── tests/                    # Тесты
```

## 🔐 Аутентификация и заголовки

### Обязательные заголовки
- **Authorization**: `tma <init_data>` - Telegram Mini App init data
- **Content-Type**: `application/json`

### Опциональные заголовки
- **X-Request-Id**: UUID v4 для отслеживания запросов в логах

### Защищенные endpoints
- Все API endpoints (`/v1/*`) требуют Telegram авторизацию
- Документация (`/docs`, `/redoc`) защищена базовой HTTP аутентификацией
- Health check (`/`) доступен без авторизации

## 📝 Работа с сущностями

### Добавление новой сущности

1. **Модель** (`app/db/models/entity.py`):
```python
class Entity(Base):
    __tablename__ = "entities"
    id = Column(String, primary_key=True, index=True)
    # ... поля
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
```

2. **Схемы** (`app/schemas/entity.py`):
```python
class EntityBase(BaseModel):
    # ... поля

class EntityCreate(EntityBase):
    pass

class EntityUpdate(BaseModel):
    # ... опциональные поля

class EntityInDBBase(EntityBase):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}

class Entity(EntityInDBBase):
    pass
```

3. **CRUD** (`app/db/crud/entity.py`):
```python
def create_entity(db: Session, entity_in: EntityCreate) -> Entity:
    # ... логика создания

def get_entity(db: Session, entity_id: str) -> Optional[Entity]:
    # ... логика получения

# ... другие CRUD операции
```

4. **API endpoints** (`app/api/v1/endpoints/entity.py`):
```python
@router.post("/", response_model=Entity)
async def create_entity(entity_in: EntityCreate, request: Request, db: Session = Depends(get_db)):
    # ... логика с проверкой авторизации

@router.get("/{entity_id}", response_model=Entity)
async def get_entity(entity_id: str, db: Session = Depends(get_db)):
    # ... логика получения
```

5. **Тесты** (`app/tests/test_entity.py`):
```python
def test_create_entity_valid(client: TestClient):
    # ... тесты с авторизацией

def test_get_entity_valid(client: TestClient):
    # ... тесты
```

6. **Миграция** (`alembic/versions/xxx_create_entity_table.py`):
```python
def upgrade():
    op.create_table("entities", ...)

def downgrade():
    op.drop_table("entities")
```

7. **Регистрация**:
- Добавить импорты в `__init__.py` файлы
- Подключить роутер в `app/api/v1/__init__.py`

## 📁 Работа с файлами

### Загрузка файлов

API поддерживает загрузку изображений с автоматической обработкой:

- **Поддерживаемые форматы**: JPEG, PNG, BMP, TIFF (GIF не поддерживается)
- **Автоматическая конвертация**: Все изображения конвертируются в WebP
- **Автоматическое изменение размера**: Максимальный размер по длинной стороне - 1024px
- **Хранение**: Файлы сохраняются в S3-совместимом хранилище

### Endpoints для файлов

#### Загрузка файла
```http
POST /v1/files/upload
Content-Type: multipart/form-data
Authorization: tma <init_data>

file: <image_file>
file_type: avatar|event
```

#### Получение списка файлов пользователя
```http
GET /v1/files/
Authorization: tma <init_data>

# Опциональные параметры:
file_type: avatar|event
skip: 0
limit: 100
```

#### Получение конкретного файла
```http
GET /v1/files/{file_id}
Authorization: tma <init_data>
```

#### Удаление файла
```http
DELETE /v1/files/{file_id}
Authorization: tma <init_data>
```

### Примеры использования

#### Python
```python
import requests

# Загрузка файла
with open("profile_photo.jpg", "rb") as f:
    files = {"file": f}
    data = {"file_type": "avatar"}
    response = requests.post(
        "http://localhost:8000/v1/files/upload",
        files=files,
        data=data,
        headers={"Authorization": "tma <init_data>"}
    )
    print(response.json())

# Получение файлов пользователя
response = requests.get(
    "http://localhost:8000/v1/files/",
    headers={"Authorization": "tma <init_data>"}
)
print(response.json())
```

#### JavaScript/Vue.js
```javascript
const uploadFile = async (file, fileType = 'avatar') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('file_type', fileType);

  const response = await fetch('/v1/files/upload', {
    method: 'POST',
    headers: { 'Authorization': 'tma <init_data>' },
    body: formData
  });
  return await response.json();
};

const getMyFiles = async (fileType = null) => {
  const params = new URLSearchParams();
  if (fileType) params.append('file_type', fileType);

  const response = await fetch(`/v1/files/?${params}`, {
    headers: { 'Authorization': 'tma <init_data>' }
  });
  return await response.json();
};
```

### Настройка S3

Для работы с файлами необходимо настроить S3-совместимое хранилище:

```env
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_BUCKET=your_bucket_name
S3_ENDPOINT_URL=https://your-s3-endpoint.com
S3_PUBLIC_URL=https://your-public-url.com
S3_REGION=us-east-1
```

### Безопасность файлов

- Пользователи могут загружать только изображения (не GIF)
- Все файлы автоматически конвертируются в WebP для оптимизации
- Пользователи могут управлять только своими файлами
- Файлы хранятся с публичным доступом для чтения

## 📊 Логирование

### Автоматическое логирование
- Все входящие запросы и ответы
- Request ID для отслеживания
- User ID из Telegram авторизации
- Время выполнения запросов
- Статус коды и размеры ответов

### Формат логов
```
Request started: {
    "request_id": "uuid",
    "method": "POST",
    "url": "/v1/profiles/",
    "user_id": 123456789,
}

Request completed: {
    "request_id": "uuid",
    "status_code": 201,
    "process_time": "0.1234s"
}
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
pytest -v

# Конкретный тест
pytest app/tests/test_profiles.py::test_create_profile_valid -v

# С покрытием
pytest --cov=app
```

### Структура тестов
- **Unit тесты**: Тестирование отдельных функций
- **Integration тесты**: Тестирование API endpoints
- **Auth тесты**: Тестирование авторизации
- **CRUD тесты**: Полный цикл операций

### Тестовые данные
- Используется `create_test_init_data()` для генерации валидных Telegram init data
- Mock Redis для тестирования
- Изолированные тестовые сессии БД

## 🚀 Запуск

###
```bash
docker compose up -d --build
```

## 🔧 Конфигурация

### Переменные окружения
```env
BOT_TOKEN=your_telegram_bot_token
DOCS_USERNAME=admin
DOCS_PASSWORD=your_password
DATABASE_URL=postgresql://user:pass@localhost/db
```

### Настройки логирования
- Уровень: INFO
- Формат: JSON
- Выход: stdout/stderr

## 📚 Документация

- **Swagger UI**: `/docs` (требует авторизацию)
- **ReDoc**: `/redoc` (требует авторизацию)
- **OpenAPI**: `/openapi.json` (требует авторизацию)

## 🔒 Безопасность

- Telegram Mini App авторизация для всех API endpoints
- Базовая HTTP аутентификация для документации
- Валидация входных данных через Pydantic
- Проверка владения ресурсами (только свои профили)
- Логирование всех операций для аудита

## 📈 CI/CD

- Автоматические тесты на GitHub Actions
- Линтинг кода (ruff, black, isort)
- Проверка типов
- Автоматическое развертывание

## 🤝 Разработка

### Code Style
- Black для форматирования
- Ruff для линтинга
- isort для сортировки импортов
- Type hints обязательны

### Git Workflow
1. Создать feature branch
2. Написать код и тесты
3. Пройти линтинг и тесты
4. Создать Pull Request
5. Code review
6. Merge в main

## 🔧 Настройка pre-commit

1. **Установите `pre-commit`**:

```bash
pip install pre-commit ruff black isort
```

2.**Установите хуки**:
```bash
pre-commit install
```
Это настроит запуск проверок перед каждым git commit.

3. **[опционально] Проверьте работу вручную (по всем файлам)**:
```bash
pre-commit run --all-files
```
