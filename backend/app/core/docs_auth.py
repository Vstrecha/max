"""
Documentation Authentication
Middleware for protecting Swagger and ReDoc documentation with basic auth.

Protects:
- /docs (Swagger UI)
- /redoc (ReDoc)
- /openapi.json (OpenAPI schema)
"""

# --------------------------------------------------------------------------------

import base64

from fastapi import Request, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings

# --------------------------------------------------------------------------------


class DocsAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for protecting documentation endpoints with basic authentication.

    Protects:
    - /docs (Swagger UI)
    - /redoc (ReDoc)
    - /openapi.json (OpenAPI schema)
    """

    async def dispatch(self, request: Request, call_next):
        """
        Check authentication for documentation endpoints.

        Args:
            request: Incoming FastAPI request
            call_next: Next middleware or endpoint handler

        Returns:
            Response: The response from the application
        """
        # Check if this is a documentation endpoint that needs protection
        path = request.url.path
        if path in ["/docs", "/redoc", "/openapi.json"]:
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Basic "):
                # Return 401 with WWW-Authenticate header
                return Response(
                    content="Authentication required",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Basic realm=Documentation"},
                    media_type="text/plain",
                )

            try:
                # Decode credentials
                credentials = base64.b64decode(auth_header[6:]).decode()
                username, password = credentials.split(":", 1)

                # Check credentials
                if username == settings.DOCS_USERNAME and password == settings.DOCS_PASSWORD:
                    return await call_next(request)
                else:
                    return Response(
                        content="Invalid credentials",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        headers={"WWW-Authenticate": "Basic realm=Documentation"},
                        media_type="text/plain",
                    )

            except Exception:
                return Response(
                    content="Invalid authentication header",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Basic realm=Documentation"},
                    media_type="text/plain",
                )

        # For non-documentation endpoints, proceed normally
        return await call_next(request)
