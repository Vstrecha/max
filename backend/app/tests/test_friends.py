"""
Friends Tests
Test cases for friends and invitations API endpoints.
"""

# --------------------------------------------------------------------------------

from fastapi.testclient import TestClient

from app.core.config import settings

# --------------------------------------------------------------------------------


def test_friends_endpoints_require_auth(client: TestClient) -> None:
    """
    Test that friends endpoints require Telegram authorization.
    """
    # Test without Authorization header
    response = client.get(f"{settings.API_VERSION}/friends/my")
    assert response.status_code == 403
    assert "Authorization header required" in response.json()["detail"]

    response = client.get(f"{settings.API_VERSION}/friends/secondary")
    assert response.status_code == 403

    response = client.get(f"{settings.API_VERSION}/friends/new")
    assert response.status_code == 403

    response = client.get(f"{settings.API_VERSION}/friends/check/test-id")
    assert response.status_code == 403

    response = client.post(f"{settings.API_VERSION}/friends/new", json={"invitation_id": "test"})
    assert response.status_code == 403


def test_friends_endpoints_invalid_auth(client: TestClient) -> None:
    """
    Test that friends endpoints reject invalid authorization.
    """
    # Test with invalid Authorization format
    response = client.get(
        f"{settings.API_VERSION}/friends/my", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 403
    assert "Invalid authorization format" in response.json()["detail"]

    response = client.get(
        f"{settings.API_VERSION}/friends/secondary", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 403

    response = client.get(
        f"{settings.API_VERSION}/friends/new", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 403

    response = client.get(
        f"{settings.API_VERSION}/friends/check/test-id", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 403

    response = client.post(
        f"{settings.API_VERSION}/friends/new",
        json={"invitation_id": "test"},
        headers={"Authorization": "Bearer token"},
    )
    assert response.status_code == 403


def test_friends_endpoints_invalid_init_data(client: TestClient) -> None:
    """
    Test that friends endpoints reject invalid init data.
    """
    # Test with invalid init data
    response = client.get(
        f"{settings.API_VERSION}/friends/my", headers={"Authorization": "tma invalid_data"}
    )
    assert response.status_code == 403
    assert "Invalid or expired Telegram init data" in response.json()["detail"]

    response = client.get(
        f"{settings.API_VERSION}/friends/secondary", headers={"Authorization": "tma invalid_data"}
    )
    assert response.status_code == 403

    response = client.get(
        f"{settings.API_VERSION}/friends/new", headers={"Authorization": "tma invalid_data"}
    )
    assert response.status_code == 403

    response = client.get(
        f"{settings.API_VERSION}/friends/check/test-id",
        headers={"Authorization": "tma invalid_data"},
    )
    assert response.status_code == 403

    response = client.post(
        f"{settings.API_VERSION}/friends/new",
        json={"invitation_id": "test"},
        headers={"Authorization": "tma invalid_data"},
    )
    assert response.status_code == 403


def test_delete_friends_endpoint_requires_auth(client: TestClient) -> None:
    """
    Test that delete friends endpoint requires Telegram authorization.
    """
    # Test without Authorization header
    response = client.delete(f"{settings.API_VERSION}/friends/test-profile-id")
    assert response.status_code == 403
    assert "Authorization header required" in response.json()["detail"]

    # Test with invalid Authorization format
    response = client.delete(
        f"{settings.API_VERSION}/friends/test-profile-id", headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 403
    assert "Invalid authorization format" in response.json()["detail"]

    # Test with invalid init data
    response = client.delete(
        f"{settings.API_VERSION}/friends/test-profile-id",
        headers={"Authorization": "tma invalid_data"},
    )
    assert response.status_code == 403
    assert "Invalid or expired Telegram init data" in response.json()["detail"]
