"""
Test Configuration
Pytest configuration and fixtures for testing the application.
"""

# --------------------------------------------------------------------------------

import os

os.environ["TESTING"] = "true"

import hashlib
import hmac
import json
import re
import tempfile
import time
import urllib.parse
from collections.abc import Generator
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from ..db.base_class import Base
from ..db.session import SessionLocal, engine
from ..main import app

# --------------------------------------------------------------------------------


def get_db():
    """
    Provide a database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables only if we have a valid engine
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # Skip table creation if database is not available
    pass


# --------------------------------------------------------------------------------


class MockRedis:
    """Mock Redis client for testing."""

    def __init__(self):
        self._storage = {}

    async def get(self, key: str) -> str | None:
        """Get value by key."""
        return self._storage.get(key)

    async def set(self, key: str, value: str, ex: int = None) -> bool:
        """Set key-value pair."""
        self._storage[key] = value
        return True

    async def delete(self, key: str) -> int:
        """Delete key."""
        if key in self._storage:
            del self._storage[key]
            return 1
        return 0

    async def scan_iter(self, match: str = None) -> list:
        """Scan keys matching pattern."""
        keys = list(self._storage.keys())
        if match:
            pattern = match.replace("*", ".*")
            keys = [k for k in keys if re.match(pattern, k)]
        return keys

    async def delete_many(self, keys: list) -> int:
        """Delete multiple keys."""
        deleted = 0
        for key in keys:
            if key in self._storage:
                del self._storage[key]
                deleted += 1
        return deleted


# --------------------------------------------------------------------------------


def override_get_db():
    """Override database session for testing."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# --------------------------------------------------------------------------------


def create_test_init_data(user_id: int = 123456789, bot_token: str = "test_token") -> str:
    """
    Create test init data for testing purposes.

    Args:
        user_id: Max user ID
        bot_token: Bot token for signing

    Returns:
        Valid init data string
    """
    auth_date = int(time.time())
    user_data = {"id": user_id, "first_name": "Test", "last_name": "User"}

    # Create data string
    data = {"auth_date": str(auth_date), "user": json.dumps(user_data), "query_id": "test_query_id"}

    # Create data check string
    pairs = [f"{k}={v}" for k, v in data.items()]
    pairs.sort()
    data_check_string = "\n".join(pairs)

    # Create secret key
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()

    # Create hash
    calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Add hash to data
    data["hash"] = calc_hash

    # Return as query string
    return urllib.parse.urlencode(data)


# --------------------------------------------------------------------------------


@pytest.fixture(scope="session")
def temp_upload_dir() -> Generator[Path, None, None]:
    """Create temporary directory for file uploads."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="session")
def admin_token() -> str:
    """Generate admin JWT token for testing."""
    # Create a simple admin token for testing
    # In real implementation, this would be a proper JWT token
    return "admin_test_token_12345"


@pytest.fixture(scope="session")
def user_token() -> str:
    """Generate user JWT token for testing."""
    # Create a simple user token for testing
    return "user_test_token_67890"


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """Create test client with overridden dependencies."""
    # Override database session
    app.dependency_overrides[get_db] = override_get_db

    # Override S3 client dependency
    from app.api.v1.endpoints.files import get_s3_client

    def mock_get_s3_client():
        """Mock S3 client for testing."""
        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_client.upload_file.return_value = "https://storage.example.com/avatars/test.webp"
        return mock_client

    app.dependency_overrides[get_s3_client] = mock_get_s3_client

    # Override Redis client
    mock_redis = MockRedis()
    app.state.redis = mock_redis

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def use_mock_redis():
    """Automatically use mock Redis for all tests."""
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    yield mock_redis


# --------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def sample_event_data():
    return {
        "name": "Test Event",
        "short_name": "TE",
        "description": "desc",
        "place": "place",
        "date": datetime.now().isoformat(),
        "type": "bc",
    }


@pytest.fixture(scope="function")
def clean_db():
    """
    Clean database between tests.
    """
    from ..db.crud.files import delete_all_files
    from ..db.crud.friends import delete_all_friends
    from ..db.crud.invitations import delete_all_invitations
    from ..db.crud.profiles import delete_all_profiles

    db = SessionLocal()
    try:
        # Delete all data in reverse order of dependencies
        delete_all_friends(db)
        delete_all_invitations(db)
        delete_all_profiles(db)
        delete_all_files(db)
        db.commit()
        yield
    finally:
        db.close()
