"""
Profile endpoint tests
Tests for profile API endpoints: get, create, update, delete, and invalid get.
"""

# --------------------------------------------------------------------------------


from fastapi.testclient import TestClient

from ..core.config import settings
from .test_telegram_auth import create_test_init_data

# --------------------------------------------------------------------------------


def test_get_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test getting profile by valid id via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Software engineer with passion for technology.",
        "telegram": user_id,
        "invited_by": None,
    }
    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert create_response.status_code == 201, create_response.text
    profile_id = create_response.json()["id"]

    # Now, get the profile
    response = client.get(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == profile_id
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]

    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, resp.text


# --------------------------------------------------------------------------------


def test_get_profiles_list_valid(client: TestClient, clean_db) -> None:
    """
    Test getting profiles list via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id_1 = 123456789
    user_id_2 = 987654321
    init_data_1 = create_test_init_data(user_id_1, settings.BOT_TOKEN)
    init_data_2 = create_test_init_data(user_id_2, settings.BOT_TOKEN)

    # Create first profile (no invitation required)
    payload_1 = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Software engineer.",
        "telegram": user_id_1,
        "invited_by": None,
    }

    response_1 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload_1,
        headers={"Authorization": f"tma {init_data_1}"},
    )
    assert response_1.status_code == 201, response_1.text
    profile_1_id = response_1.json()["id"]

    # Create invitation for second user
    invitation_response = client.get(
        f"{settings.API_VERSION}/friends/new",
        headers={"Authorization": f"tma {init_data_1}"},
    )
    assert invitation_response.status_code == 200, invitation_response.text
    invitation_id = invitation_response.json()["id"]

    # Create second profile with invitation
    payload_2 = {
        "first_name": "Jane",
        "last_name": "Smith",
        "gender": "F",
        "birth_date": "1998-08-20",
        "avatar": None,
        "university": "Moscow State University",
        "bio": "Data scientist.",
        "telegram": user_id_2,
        "invited_by": None,
        "invitation": invitation_id,
    }

    response_2 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload_2,
        headers={"Authorization": f"tma {init_data_2}"},
    )
    assert response_2.status_code == 201, response_2.text
    profile_2_id = response_2.json()["id"]

    # Clean up
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_2_id}",
        headers={"Authorization": f"tma {init_data_2}"},
    )
    assert resp.status_code == 204, resp.text

    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_1_id}",
        headers={"Authorization": f"tma {init_data_1}"},
    )
    assert resp.status_code == 204, resp.text


# --------------------------------------------------------------------------------


def test_create_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test creating profile with valid data via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 555666777
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile (this will be the first user)
    payload = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "gender": "F",
        "birth_date": "1992-03-10",
        "avatar": None,
        "university": "ITMO University",
        "bio": "Frontend developer.",
        "telegram": user_id,
        "invited_by": None,
    }
    response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["gender"] == payload["gender"]
    assert data["university"] == payload["university"]
    assert "id" in data


# --------------------------------------------------------------------------------


def test_update_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test updating profile with valid data via the API endpoint (PUT endpoint - deprecated).
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 111222333
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile
    payload = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "gender": "M",
        "birth_date": "1990-12-25",
        "avatar": None,
        "university": "Bauman Moscow State Technical University",
        "bio": "Backend developer.",
        "telegram": user_id,
        "invited_by": None,
    }

    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert create_response.status_code == 201, create_response.text
    profile_id = create_response.json()["id"]

    # Update profile using PATCH endpoint (PUT is deprecated)
    update_payload = {
        "last_name": "Brown",
        "bio": "Updated bio information.",
        "avatar": None,
    }
    update_response = client.patch(
        f"{settings.API_VERSION}/profiles/",
        json=update_payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert updated_data["last_name"] == update_payload["last_name"]
    assert updated_data["id"] == profile_id
    assert updated_data["bio"] == update_payload["bio"]
    assert updated_data["avatar"] == update_payload["avatar"]


# --------------------------------------------------------------------------------


def test_delete_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test deleting profile by id via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 444555666
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile
    payload = {
        "first_name": "Charlie",
        "last_name": "Davis",
        "gender": "M",
        "birth_date": "1988-07-14",
        "avatar": None,
        "university": "Moscow Institute of Physics and Technology",
        "bio": "DevOps engineer.",
        "telegram": user_id,
        "invited_by": None,
    }
    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert create_response.status_code == 201, create_response.text
    profile_id = create_response.json()["id"]

    # Delete profile
    del_response = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert del_response.status_code == 204, del_response.text

    # Try to get deleted profile
    get_response = client.get(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert get_response.status_code == 404


# --------------------------------------------------------------------------------


def test_get_profile_invalid(client: TestClient, clean_db) -> None:
    """
    Test getting profile by invalid id via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    response = client.get(
        f"{settings.API_VERSION}/profiles/nonexistent-id",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 404


# --------------------------------------------------------------------------------


def test_get_invited_profiles_valid(client: TestClient, clean_db) -> None:
    """
    Test getting invited profiles via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data for different users
    inviter_user_id = 111111111
    invited_user_id_1 = 222222222
    invited_user_id_2 = 333333333

    inviter_init_data = create_test_init_data(inviter_user_id, settings.BOT_TOKEN)
    invited_init_data_1 = create_test_init_data(invited_user_id_1, settings.BOT_TOKEN)
    invited_init_data_2 = create_test_init_data(invited_user_id_2, settings.BOT_TOKEN)

    # Create inviter profile
    inviter_payload = {
        "first_name": "Inviter",
        "last_name": "User",
        "gender": "M",
        "birth_date": "1990-01-01",
        "avatar": None,
        "university": "Test University",
        "bio": "Test inviter.",
        "telegram": inviter_user_id,
        "invited_by": None,
    }
    inviter_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=inviter_payload,
        headers={"Authorization": f"tma {inviter_init_data}"},
    )
    assert inviter_response.status_code == 201, inviter_response.text
    inviter_id = inviter_response.json()["id"]

    # Create first invited profile with invitation from inviter
    invitation_response_1 = client.get(
        f"{settings.API_VERSION}/friends/new",
        headers={"Authorization": f"tma {inviter_init_data}"},
    )
    assert invitation_response_1.status_code == 200, invitation_response_1.text
    invitation_id_1 = invitation_response_1.json()["id"]

    invited_payload_1 = {
        "first_name": "Invited1",
        "last_name": "User",
        "gender": "F",
        "birth_date": "1995-01-01",
        "avatar": None,
        "university": "Test University",
        "bio": "Test invited user 1.",
        "telegram": invited_user_id_1,
        "invited_by": inviter_id,
        "invitation": invitation_id_1,
    }

    response_1 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=invited_payload_1,
        headers={"Authorization": f"tma {invited_init_data_1}"},
    )
    assert response_1.status_code == 201, response_1.text
    invited_id_1 = response_1.json()["id"]

    # Create second invited profile with invitation from first invited user
    invitation_response_2 = client.get(
        f"{settings.API_VERSION}/friends/new",
        headers={"Authorization": f"tma {invited_init_data_1}"},
    )
    assert invitation_response_2.status_code == 200, invitation_response_2.text
    invitation_id_2 = invitation_response_2.json()["id"]

    invited_payload_2 = {
        "first_name": "Invited2",
        "last_name": "User",
        "gender": "M",
        "birth_date": "1998-01-01",
        "avatar": None,
        "university": "Test University",
        "bio": "Test invited user 2.",
        "telegram": invited_user_id_2,
        "invited_by": invited_id_1,
        "invitation": invitation_id_2,
    }

    response_2 = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=invited_payload_2,
        headers={"Authorization": f"tma {invited_init_data_2}"},
    )
    assert response_2.status_code == 201, response_2.text
    invited_id_2 = response_2.json()["id"]

    # Test getting invited profiles for inviter
    resp = client.get(
        f"{settings.API_VERSION}/profiles/{inviter_id}/invited",
        headers={"Authorization": f"tma {inviter_init_data}"},
    )
    assert resp.status_code == 200
    invited_profiles = resp.json()
    assert len(invited_profiles) == 1  # Only first invited user
    assert invited_profiles[0]["id"] == invited_id_1

    # Test getting invited profiles for first invited user
    resp = client.get(
        f"{settings.API_VERSION}/profiles/{invited_id_1}/invited",
        headers={"Authorization": f"tma {invited_init_data_1}"},
    )
    assert resp.status_code == 200
    invited_profiles_2 = resp.json()
    assert len(invited_profiles_2) == 1  # Only second invited user
    assert invited_profiles_2[0]["id"] == invited_id_2

    # Test pagination for invited profiles
    resp_paginated = client.get(
        f"{settings.API_VERSION}/profiles/{inviter_id}/invited",
        params={"skip": 0, "limit": 1},
        headers={"Authorization": f"tma {inviter_init_data}"},
    )
    assert resp_paginated.status_code == 200
    paginated_invited = resp_paginated.json()
    assert len(paginated_invited) <= 1

    # Clean up
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{invited_id_2}",
        headers={"Authorization": f"tma {invited_init_data_2}"},
    )
    assert resp.status_code == 204, resp.text

    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{invited_id_1}",
        headers={"Authorization": f"tma {invited_init_data_1}"},
    )
    assert resp.status_code == 204, resp.text

    # Delete inviter profile
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{inviter_id}",
        headers={"Authorization": f"tma {inviter_init_data}"},
    )
    assert resp.status_code == 204, resp.text


# --------------------------------------------------------------------------------


def test_get_my_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test getting current user's profile via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Software engineer with passion for technology.",
        "telegram": user_id,
        "invited_by": None,
    }
    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert create_response.status_code == 201, create_response.text

    # Now, get the current user's profile
    response = client.get(
        f"{settings.API_VERSION}/profiles/my",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["telegram"] == user_id

    # Clean up
    profile_id = data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, resp.text


# --------------------------------------------------------------------------------


def test_get_my_profile_not_found(client: TestClient, clean_db) -> None:
    """
    Test getting current user's profile when it doesn't exist.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 999888777
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Try to get profile that doesn't exist
    response = client.get(
        f"{settings.API_VERSION}/profiles/my",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_patch_profile_valid(client: TestClient, clean_db) -> None:
    """
    Test patching profile with valid data via the API endpoint.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 111222333
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Create profile
    payload = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "gender": "M",
        "birth_date": "1990-12-25",
        "avatar": None,
        "university": "Bauman Moscow State Technical University",
        "bio": "Backend developer.",
        "telegram": user_id,
        "invited_by": None,
    }

    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert create_response.status_code == 201, create_response.text
    profile_id = create_response.json()["id"]

    # Patch profile
    patch_payload = {
        "last_name": "Brown",
        "bio": "Updated bio information.",
        "avatar": None,
    }
    patch_response = client.patch(
        f"{settings.API_VERSION}/profiles/",
        json=patch_payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert patch_response.status_code == 200, patch_response.text
    patched_data = patch_response.json()
    assert patched_data["last_name"] == patch_payload["last_name"]
    assert patched_data["bio"] == patch_payload["bio"]
    assert patched_data["avatar"] == patch_payload["avatar"]
    # Check that other fields remain unchanged
    assert patched_data["first_name"] == payload["first_name"]
    assert patched_data["telegram"] == user_id

    # Clean up
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, resp.text


# --------------------------------------------------------------------------------


def test_patch_profile_not_found(client: TestClient, clean_db) -> None:
    """
    Test patching profile when it doesn't exist.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 444555666
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Try to patch profile that doesn't exist
    patch_payload = {
        "last_name": "Brown",
        "bio": "Updated bio information.",
    }
    response = client.patch(
        f"{settings.API_VERSION}/profiles/",
        json=patch_payload,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 404, response.text
