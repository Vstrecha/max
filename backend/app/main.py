"""
Main Application
Entry point and FastAPI app configuration.
"""

# --------------------------------------------------------------------------------

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import api_router
from .core.config import settings
from .core.docs_auth import DocsAuthMiddleware
from .core.log_config import logger, setup_logging
from .core.max_auth_middleware import MaxAuthMiddleware
from .core.middleware import RequestLoggingMiddleware

# --------------------------------------------------------------------------------

# Patch FastAPI's _remap_definitions_and_field_mappings to handle missing $ref
# This is a workaround for a known issue in FastAPI with Pydantic v2
try:
    from fastapi._compat import v2 as fastapi_v2_compat

    original_remap = fastapi_v2_compat._remap_definitions_and_field_mappings

    def patched_remap(*, model_name_map, definitions, field_mapping):
        try:
            return original_remap(
                model_name_map=model_name_map,
                definitions=definitions,
                field_mapping=field_mapping,
            )
        except KeyError as e:
            if str(e) == "'$ref'":
                # If $ref is missing, try to continue with existing mappings
                # Filter out problematic schemas and continue
                logger.warning("Skipping schema with missing $ref in FastAPI compatibility layer")
                # Return original mappings to continue processing
                return field_mapping, definitions
            raise

    fastapi_v2_compat._remap_definitions_and_field_mappings = patched_remap

    # Also patch get_schema_from_model_field to handle missing field_mapping
    original_get_schema = fastapi_v2_compat.get_schema_from_model_field

    def patched_get_schema(
        *, field, model_name_map, field_mapping, separate_input_output_schemas=True
    ):
        try:
            return original_get_schema(
                field=field,
                model_name_map=model_name_map,
                field_mapping=field_mapping,
                separate_input_output_schemas=separate_input_output_schemas,
            )
        except KeyError:
            # If field_mapping is missing, try to generate schema directly
            # Try different mode combinations
            for mode in ["serialization", "validation"]:
                key = (field, mode)
                if key in field_mapping:
                    return field_mapping[key]

            logger.warning(
                f"Missing field_mapping for {field.name}, trying direct schema generation"
            )
            try:
                # Try to get schema directly from Pydantic
                from pydantic import TypeAdapter

                adapter = TypeAdapter(field.annotation)
                schema = adapter.json_schema()
                # Add to field_mapping for future use (both modes)
                field_mapping[(field, "serialization")] = schema
                field_mapping[(field, "validation")] = schema
                return schema
            except Exception as e:
                logger.warning(f"Failed to generate schema directly: {e}")
                # Fallback: try to find similar field in mapping
                for (f, _m), s in field_mapping.items():
                    if f.annotation == field.annotation:
                        return s
                # Last resort: return empty schema
                return {}

    fastapi_v2_compat.get_schema_from_model_field = patched_get_schema
except (ImportError, AttributeError) as e:
    logger.warning(f"Could not patch FastAPI compatibility layer: {e}")

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
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    description="""
# Vstrecha API

## Request Headers

### Required Headers

**Authorization** - Max authorization
- Format: `tma <init_data>`
- Example: `Authorization: tma auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123`
- Description: Max Mini App init data for user authentication

### Optional Headers

**X-Request-Id** - Request identifier
- Format: UUID v4
- Example: `X-Request-Id: 123e4567-e89b-12d3-a456-426614174000`
- Description: Unique identifier for request tracking in logs

## Authentication

All API endpoints (except `/`) require Max authorization via the `Authorization` header.

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
    # Use cached schema if available and valid
    if app.openapi_schema:
        return app.openapi_schema

    try:
        # Use default FastAPI schema generation to avoid KeyError issues
        # Get the default openapi method from FastAPI class
        from fastapi import FastAPI as FastAPIClass

        default_openapi = FastAPIClass.openapi.__get__(app, FastAPIClass)

        # Generate using default FastAPI method
        openapi_schema = default_openapi()

        # Add tags manually after schema generation
        if app.openapi_tags:
            openapi_schema["tags"] = app.openapi_tags

        # Force OpenAPI version to 3.0.2 for compatibility
        openapi_schema["openapi"] = "3.0.2"

        # Validate schema can be serialized to JSON
        import json

        try:
            json.dumps(openapi_schema, default=str)
        except Exception as json_error:
            logger.error(f"Schema serialization error: {json_error}", exc_info=True)
            # Clear any partial schema and re-raise
            app.openapi_schema = None
            raise

        # Cache the schema only if it's valid
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except KeyError as ke:
        # Handle KeyError - this is a known issue with FastAPI's internal schema processing
        logger.error(f"KeyError in OpenAPI schema: {ke}", exc_info=True)
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        # Clear cache to force regeneration on next request
        app.openapi_schema = None
        # Return minimal working schema
        return {
            "openapi": "3.0.2",
            "info": {
                "title": app.title,
                "version": app.version,
            },
            "paths": {},
            "components": {"schemas": {}},
        }
    except Exception as e:
        logger.error(f"Error generating OpenAPI schema: {e}", exc_info=True)
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        # Clear cache to force regeneration on next request
        app.openapi_schema = None
        # Return a minimal schema if generation fails
        return {
            "openapi": "3.0.2",
            "info": {
                "title": app.title,
                "version": app.version,
            },
            "paths": {},
            "components": {"schemas": {}},
        }


# Add custom middleware first (order matters)
# В FastAPI middleware выполняются в ОБРАТНОМ порядке добавления
# Поэтому DocsAuthMiddleware добавляем ПОСЛЕДНИМ, чтобы он выполнился ПЕРВЫМ
# и обработал /docs, /redoc, /openapi.json до MaxAuthMiddleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(MaxAuthMiddleware)
app.add_middleware(DocsAuthMiddleware)  # Добавляем последним, выполнится первым

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------------

# Register API routes BEFORE setting custom OpenAPI schema
# This ensures all routes are included in the schema
app.include_router(api_router, prefix=settings.API_VERSION)

# Set custom OpenAPI schema AFTER routes are registered
app.openapi = custom_openapi


# --------------------------------------------------------------------------------


@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint for health check.

    Returns:
        dict: API status message.
    """
    return {"status": "ok", "message": "Vstrecha API is running"}
