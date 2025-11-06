"""
Telegram Authentication Middleware
Middleware for protecting API endpoints with Telegram Mini App authentication.
"""

# --------------------------------------------------------------------------------

import json
from collections.abc import Callable

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .telegram_auth import extract_telegram_auth_from_header, verify_init_data_and_get_user_id

# --------------------------------------------------------------------------------


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for protecting API endpoints with Telegram authentication.

    Features:
    - Verifies Telegram Mini App init data
    - Extracts user_id from valid init data
    - Protects all API endpoints except ping and docs
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Check Telegram authentication for protected endpoints.

        Args:
            request: Incoming FastAPI request
            call_next: Next middleware or endpoint handler

        Returns:
            Response: The response from the application
        """
        # Skip authentication for ping and documentation endpoints
        path = request.url.path
        if path in ["/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response(
                content=json.dumps({"detail": "Authorization header required"}),
                status_code=status.HTTP_403_FORBIDDEN,
                media_type="application/json",
            )

        # Extract init data from header
        init_data = extract_telegram_auth_from_header(auth_header)
        if not init_data:
            return Response(
                content=json.dumps(
                    {"detail": "Invalid authorization format. Expected: 'tma <init_data>'"}
                ),
                status_code=status.HTTP_403_FORBIDDEN,
                media_type="application/json",
            )

        # Verify init data and get user info
        user_info = verify_init_data_and_get_user_id(init_data, settings.BOT_TOKEN)
        if not user_info:
            return Response(
                content=json.dumps({"detail": "Invalid or expired Telegram init data"}),
                status_code=status.HTTP_403_FORBIDDEN,
                media_type="application/json",
            )

        # Add user_id to request state for use in endpoints
        request.state.user_id = user_info["user_id"]
        request.state.telegram_user = user_info["user"]

        return await call_next(request)
