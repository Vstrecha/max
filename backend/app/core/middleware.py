"""
Middleware
Custom middleware for request/response logging and X-Request-Id support.
"""

# --------------------------------------------------------------------------------

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .log_config import logger

# --------------------------------------------------------------------------------


def _get_client_ip(request: Request) -> str:
    """
    Get the real client IP address, handling proxy headers.

    Args:
        request: FastAPI request object

    Returns:
        str: Client IP address
    """
    # Check for forwarded headers (common in Docker/proxy setups)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, take the first one
        return forwarded_for.split(",")[0].strip()

    # Check for real IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Check for X-Forwarded header
    forwarded = request.headers.get("X-Forwarded")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Fallback to direct client IP
    if request.client:
        return request.client.host

    return "unknown"


# --------------------------------------------------------------------------------


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging all incoming requests and responses.

    Features:
    - Logs request details including X-Request-Id
    - Logs response details and timing
    - Handles X-Request-Id header gracefully
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log details.

        Args:
            request: Incoming FastAPI request
            call_next: Next middleware or endpoint handler

        Returns:
            Response: The response from the application
        """
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            request_id = str(uuid.uuid4())

        # Add request ID to request state for use in endpoints
        request.state.request_id = request_id

        # Log request details
        start_time = time.time()

        # Prepare request log data
        request_data = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query": str(request.url.query) if request.url.query else None,
        }

        # Log request body for non-GET requests (be careful with sensitive data)
        # Skip body reading for documentation endpoints to avoid consuming the stream
        if request.method not in ["GET", "HEAD", "OPTIONS"] and request.url.path not in [
            "/docs",
            "/redoc",
            "/openapi.json",
        ]:
            try:
                # Read body only if it's available and not already consumed
                if hasattr(request, "_body"):
                    body = request._body
                else:
                    body = await request.body()
                if body:
                    # Truncate body for logging (first 1000 chars)
                    body_str = body.decode()[:1000]
                    request_data["body_preview"] = body_str + ("..." if len(body) > 1000 else "")
            except Exception as e:
                request_data["body_error"] = str(e)

        # Add user_id if available (from Telegram auth)
        user_id_info = ""
        if hasattr(request.state, "user_id"):
            user_id_info = f", User: {request.state.user_id}"

        # Prepare URL info
        url_info = str(request.url)
        if request.url.query:
            url_info = f"{request.url.path}?{request.url.query}"

        # Log request details
        logger.info(
            f"Request started - ID: {request_id}, Method: {request.method}, "
            f"URL: {url_info}, IP: {_get_client_ip(request)}{user_id_info}"
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            logger.info(
                "Request completed - ID: %s, Status: %s, Time: %.4fs, Size: %s",
                request_id,
                response.status_code,
                process_time,
                response.headers.get("content-length", "unknown"),
            )

            # Add request ID to response headers
            response.headers["X-Request-Id"] = request_id

            return response

        except Exception as e:
            # Log error with full traceback
            process_time = time.time() - start_time

            logger.error(
                f"Request failed - ID: {request_id}, Error: {str(e)}, Time: {process_time:.4f}s",
                exc_info=True,
            )
            # Return error response instead of raising
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=500,
                content={"detail": f"Internal server error: {str(e)}"},
                headers={"X-Request-Id": request_id},
            )
