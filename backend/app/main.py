"""
Main Application
Entry point and FastAPI app configuration.
"""

# --------------------------------------------------------------------------------

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .api.v1 import api_router
from .core.config import settings
from .core.docs_auth import DocsAuthMiddleware
from .core.log_config import logger, setup_logging
from .core.middleware import RequestLoggingMiddleware
from .core.telegram_auth_middleware import TelegramAuthMiddleware

# --------------------------------------------------------------------------------

setup_logging()


# --------------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Args:
        app (FastAPI): FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting vstrecha application...")
    yield


# --------------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
    description="""
# Vstrecha API

## Request Headers

### Required Headers

**Authorization** - Telegram authorization
- Format: `tma <init_data>`
- Example: `Authorization: tma auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123`
- Description: Telegram Mini App init data for user authentication

### Optional Headers

**X-Request-Id** - Request identifier
- Format: UUID v4
- Example: `X-Request-Id: 123e4567-e89b-12d3-a456-426614174000`
- Description: Unique identifier for request tracking in logs

## Authentication

All API endpoints (except `/`) require Telegram authorization via the `Authorization` header.

Documentation (`/docs`, `/redoc`) is protected with basic HTTP authentication.

## Logging

All requests and responses are logged including:
- Request ID
- User ID (if available)
- Execution time
- Status code
- Response size
""",
    version=settings.VERSION,
    openapi_tags=[
        {"name": "profiles", "description": "User profile operations"},
        {"name": "files", "description": "File upload and management"},
        {"name": "friends", "description": "Friends and invitations management"},
        {"name": "events", "description": "Event management"},
    ],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )

    # Force OpenAPI version to 3.0.2 for compatibility
    openapi_schema["openapi"] = "3.0.2"

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Add custom middleware first (order matters)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(TelegramAuthMiddleware)
app.add_middleware(DocsAuthMiddleware)

# Set custom OpenAPI schema
app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------------

app.include_router(api_router, prefix=settings.API_VERSION)


# --------------------------------------------------------------------------------


@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint for health check.

    Returns:
        dict: API status message.
    """
    return {"status": "ok", "message": "Vstrecha API is running"}
