"""
API Router
Includes all version 1 API endpoint routers.
"""

# --------------------------------------------------------------------------------

from fastapi import APIRouter

from .endpoints import events, files, friends, profiles

# --------------------------------------------------------------------------------

api_router = APIRouter()

api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
