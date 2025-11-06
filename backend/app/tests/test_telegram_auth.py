"""
Telegram Authentication Tests
Tests for Telegram Mini App authentication functionality.
"""

# --------------------------------------------------------------------------------

import hashlib
import hmac
import json
import time
import urllib.parse

from fastapi.testclient import TestClient

from ..core.config import settings
from ..core.telegram_auth import extract_telegram_auth_from_header, verify_init_data_and_get_user_id

# --------------------------------------------------------------------------------


def create_test_init_data(user_id: int = 123456789, bot_token: str = "test_token") -> str:
    """
    Create test init data for testing purposes.

    Args:
        user_id: Telegram user ID
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


def test_extract_telegram_auth_from_header():
    """Test extracting init data from Authorization header."""
    # Valid header
    auth_header = "tma auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123"
    result = extract_telegram_auth_from_header(auth_header)
    assert result == "auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123"

    # Invalid header
    result = extract_telegram_auth_from_header("Bearer token")
    assert result is None

    # Empty header
    result = extract_telegram_auth_from_header("")
    assert result is None

    # None header
    result = extract_telegram_auth_from_header(None)
    assert result is None


def test_verify_init_data_and_get_user_id():
    """Test verifying init data and extracting user info."""
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Test valid init data
    result = verify_init_data_and_get_user_id(init_data, settings.BOT_TOKEN)
    assert result is not None
    assert result["user_id"] == user_id
    assert result["user"]["id"] == user_id
    assert result["user"]["first_name"] == "Test"

    # Test invalid init data
    result = verify_init_data_and_get_user_id("invalid_data", settings.BOT_TOKEN)
    assert result is None

    # Test wrong bot token
    result = verify_init_data_and_get_user_id(init_data, "wrong_token")
    assert result is None


def test_telegram_auth_middleware_unauthorized(client: TestClient):
    """Test that API endpoints require Telegram authorization."""
    # Test without Authorization header
    response = client.get("/v1/profiles/")
    assert response.status_code == 403
    assert "Authorization header required" in response.json()["detail"]

    # Test with invalid Authorization format
    response = client.get("/v1/profiles/", headers={"Authorization": "Bearer token"})
    assert response.status_code == 403
    assert "Invalid authorization format" in response.json()["detail"]

    # Test with invalid init data
    response = client.get("/v1/profiles/", headers={"Authorization": "tma invalid_data"})
    assert response.status_code == 403
    assert "Invalid or expired Telegram init data" in response.json()["detail"]


def test_telegram_auth_middleware_public_endpoints(client: TestClient):
    """Test that public endpoints don't require authorization."""
    # Test ping endpoint
    response = client.get("/")
    assert response.status_code == 200

    # Test docs endpoints (these are protected by docs auth, not telegram auth)
    response = client.get("/docs")
    assert response.status_code == 401  # Docs auth required, not telegram auth


def test_profile_creation_with_telegram_auth(client: TestClient, clean_db):
    """Test profile creation with valid Telegram authorization."""
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile with matching telegram ID
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "telegram": user_id,
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Test user",
        "invited_by": None,
    }

    response = client.post(
        "/v1/profiles/", json=payload, headers={"Authorization": f"tma {init_data}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["telegram"] == user_id


def test_profile_update_ownership(client: TestClient, clean_db):
    """Test profile update with ownership check."""
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First create a profile
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "telegram": user_id,
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Test user",
        "invited_by": None,
    }

    create_response = client.post(
        "/v1/profiles/", json=create_payload, headers={"Authorization": f"tma {init_data}"}
    )
    assert create_response.status_code == 201

    # Update profile (should work) - using PATCH endpoint
    update_payload = {"first_name": "Jane", "bio": "Updated bio"}

    update_response = client.patch(
        "/v1/profiles/",
        json=update_payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["first_name"] == "Jane"
    assert data["bio"] == "Updated bio"


def test_profile_update_unauthorized(client: TestClient, clean_db):
    """Test profile update by non-owner."""
    # Create valid init data for user 1
    user_id_1 = 123456789
    init_data_1 = create_test_init_data(user_id_1, settings.BOT_TOKEN)

    # Create valid init data for user 2
    user_id_2 = 987654321
    init_data_2 = create_test_init_data(user_id_2, settings.BOT_TOKEN)

    # Create profile for user 1
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "telegram": user_id_1,
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Test user",
        "invited_by": None,
    }

    create_response = client.post(
        "/v1/profiles/", json=create_payload, headers={"Authorization": f"tma {init_data_1}"}
    )
    assert create_response.status_code == 201

    # Try to update profile with user 2 (should fail) - using PATCH endpoint
    update_payload = {"first_name": "Jane"}

    update_response = client.patch(
        "/v1/profiles/",
        json=update_payload,
        headers={"Authorization": f"tma {init_data_2}"},
    )
    assert update_response.status_code == 404
    assert "Profile not found" in update_response.json()["detail"]


def test_profile_delete_ownership(client: TestClient, clean_db):
    """Test profile deletion with ownership check."""
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First create a profile
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "telegram": user_id,
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Test user",
        "invited_by": None,
    }

    create_response = client.post(
        "/v1/profiles/", json=create_payload, headers={"Authorization": f"tma {init_data}"}
    )
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    # Delete profile (should work)
    delete_response = client.delete(
        f"/v1/profiles/{profile_id}", headers={"Authorization": f"tma {init_data}"}
    )
    assert delete_response.status_code == 204

    # Verify profile is deleted
    get_response = client.get(
        f"/v1/profiles/{profile_id}", headers={"Authorization": f"tma {init_data}"}
    )
    assert get_response.status_code == 404
