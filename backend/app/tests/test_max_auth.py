"""
Max Authentication Tests
Tests for Max Mini App authentication functionality.
"""

# --------------------------------------------------------------------------------

import hashlib
import hmac
import json
import time
import urllib.parse

from fastapi.testclient import TestClient

from ..core.config import settings
from ..core.max_auth import extract_max_auth_from_header, verify_init_data_and_get_user_id

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


def test_extract_max_auth_from_header():
    """Test extracting init data from Authorization header."""
    auth_header = "tma auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123"
    result = extract_max_auth_from_header(auth_header)
    assert result == "auth_date=1234567890&user=%7B%22id%22%3A123456789%7D&hash=abc123"

    result = extract_max_auth_from_header("Bearer token")
    assert result is None

    result = extract_max_auth_from_header("")
    assert result is None

    result = extract_max_auth_from_header(None)
    assert result is None


def test_verify_init_data_and_get_user_id():
    """Test verifying init data and extracting user ID."""
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)
    result = verify_init_data_and_get_user_id(init_data, settings.BOT_TOKEN)
    assert result is not None
    assert result["user_id"] == user_id

    result = verify_init_data_and_get_user_id("invalid_data", settings.BOT_TOKEN)
    assert result is None


def test_max_auth_middleware_unauthorized(client: TestClient):
    """Test that API endpoints require Max authorization."""
    # Test endpoint without authorization
    response = client.get(f"{settings.API_VERSION}/profiles/my")
    assert response.status_code == 403
    assert "Authorization header required" in response.json()["detail"]

    # Test endpoint with invalid authorization
    response = client.get(
        f"{settings.API_VERSION}/profiles/my", headers={"Authorization": "tma invalid_data"}
    )
    assert response.status_code == 403
    assert "Invalid or expired Max init data" in response.json()["detail"]


def test_max_auth_middleware_public_endpoints(client: TestClient):
    """Test that public endpoints don't require Max authorization."""
    # Test root endpoint
    response = client.get("/")
    assert response.status_code == 200

    # Test docs endpoints (these are protected by docs auth, not max auth)
    response = client.get("/docs")
    assert response.status_code == 401  # Docs auth required, not max auth


def test_profile_creation_with_max_auth(client: TestClient, clean_db):
    """Test profile creation with valid Max authorization."""
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile with matching max ID
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1990-01-01",
        "university": "Test University",
        "max_id": user_id,
    }
    response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["max_id"] == user_id


def test_profile_access_with_max_auth(client: TestClient, clean_db):
    """Test accessing profile with valid Max authorization."""
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1990-01-01",
        "university": "Test University",
        "max_id": user_id,
    }
    client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )

    # Access profile
    response = client.get(
        f"{settings.API_VERSION}/profiles/my", headers={"Authorization": f"tma {init_data}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["max_id"] == user_id


def test_multiple_users_with_max_auth(client: TestClient, clean_db):
    """Test multiple users with different Max IDs."""
    user_id_1 = 111111111
    user_id_2 = 222222222
    init_data_1 = create_test_init_data(user_id_1, settings.BOT_TOKEN)
    init_data_2 = create_test_init_data(user_id_2, settings.BOT_TOKEN)

    # Create profiles for both users
    payload_1 = {
        "first_name": "User",
        "last_name": "One",
        "gender": "M",
        "birth_date": "1990-01-01",
        "university": "Test University",
        "max_id": user_id_1,
    }
    payload_2 = {
        "first_name": "User",
        "last_name": "Two",
        "gender": "F",
        "birth_date": "1991-01-01",
        "university": "Test University",
        "max_id": user_id_2,
    }

    response_1 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload_1,
        headers={"Authorization": f"tma {init_data_1}"},
    )
    response_2 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload_2,
        headers={"Authorization": f"tma {init_data_2}"},
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    # Verify each user can only access their own profile
    response_1 = client.get(
        f"{settings.API_VERSION}/profiles/my", headers={"Authorization": f"tma {init_data_1}"}
    )
    response_2 = client.get(
        f"{settings.API_VERSION}/profiles/my", headers={"Authorization": f"tma {init_data_2}"}
    )

    assert response_1.json()["max_id"] == user_id_1
    assert response_2.json()["max_id"] == user_id_2


def test_profile_update_with_max_auth(client: TestClient, clean_db):
    """Test updating profile with valid Max authorization."""
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1990-01-01",
        "university": "Test University",
        "max_id": user_id,
    }
    client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )

    # Update profile
    update_payload = {"first_name": "Jane"}
    response = client.patch(
        f"{settings.API_VERSION}/profiles/",
        json=update_payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["max_id"] == user_id
