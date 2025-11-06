"""
File endpoint tests
Tests for file API endpoints: upload, get, delete.
"""

# --------------------------------------------------------------------------------

import io

from fastapi.testclient import TestClient
from PIL import Image

from ..core.config import settings
from .test_max_auth import create_test_init_data

# --------------------------------------------------------------------------------


def create_profile_with_invite(client: TestClient, user_id: int, init_data: str) -> dict:
    """
    Create a profile with invite for testing.

    Args:
        client (TestClient): FastAPI test client.
        user_id (int): User Max ID.
        init_data (str): Max init data.

    Returns:
        dict: Profile data.
    """
    # Create profile payload
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "M",
        "birth_date": "1995-05-15",
        "avatar": None,
        "university": "HSE University",
        "bio": "Software engineer with passion for technology.",
        "max_id": user_id,
        "invitation": None,
    }

    # Try to create profile first (works if this is the first user)
    create_response = client.post(
        f"{settings.API_VERSION}/profiles/",
        json=payload,
        headers={"Authorization": f"tma {init_data}"},
    )

    if create_response.status_code == 400 and "Invitation ID is required" in create_response.text:
        # Need an invitation - try to create first user or use existing invitation

        # Try to create the first user who doesn't need an invitation
        first_user_id = 999999999  # Special ID for first user
        first_init_data = create_test_init_data(first_user_id, settings.BOT_TOKEN)
        first_payload = payload.copy()
        first_payload["max_id"] = first_user_id

        first_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=first_payload,
            headers={"Authorization": f"tma {first_init_data}"},
        )

        if first_response.status_code == 201:
            # Successfully created first user
            first_user_data = first_response.json()
        else:
            # First user already exists, try to get any existing profile to create invitation
            # We'll use user ID 999999999 as our default inviter
            first_user_data = {"max_id": first_user_id}

        # Create invitation from the first user
        first_init_data = create_test_init_data(first_user_data["max_id"], settings.BOT_TOKEN)
        invite_response = client.post(
            f"{settings.API_VERSION}/profiles/invitations/",
            headers={"Authorization": f"tma {first_init_data}"},
        )

        if invite_response.status_code == 201:
            invitation_id = invite_response.json()["id"]
            payload["invitation"] = invitation_id

            # Try again with invitation
            create_response = client.post(
                f"{settings.API_VERSION}/profiles/",
                json=payload,
                headers={"Authorization": f"tma {init_data}"},
            )
        else:
            # If invitation creation failed, try to get existing invitations
            invitations_response = client.get(
                f"{settings.API_VERSION}/profiles/invitations/",
                headers={"Authorization": f"tma {first_init_data}"},
            )

            if invitations_response.status_code == 200:
                invitations = invitations_response.json()
                if invitations:
                    # Use the first available invitation
                    payload["invitation"] = invitations[0]["id"]
                    create_response = client.post(
                        f"{settings.API_VERSION}/profiles/",
                        json=payload,
                        headers={"Authorization": f"tma {init_data}"},
                    )

    assert create_response.status_code == 201, create_response.text
    return create_response.json()


def create_test_image(width: int = 100, height: int = 100, format: str = "JPEG") -> io.BytesIO:
    """
    Create a test image for testing purposes.

    Args:
        width (int): Image width.
        height (int): Image height.
        format (str): Image format.

    Returns:
        io.BytesIO: Image bytes.
    """
    image = Image.new("RGB", (width, height), color="red")
    img_io = io.BytesIO()
    image.save(img_io, format=format)
    img_io.seek(0)
    return img_io


# --------------------------------------------------------------------------------


def test_upload_file_valid(client: TestClient, clean_db) -> None:
    """
    Test uploading a valid image file.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    profile_data = create_profile_with_invite(client, user_id, init_data)

    # Create test image
    test_image = create_test_image()

    # Upload file
    files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
    data = {"file_type": "avatar"}

    response = client.post(
        f"{settings.API_VERSION}/files/upload",
        files=files,
        data=data,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert "url" in data
    assert data["url"].startswith("https://")
    assert ".webp" in data["url"]

    # Clean up
    file_id = data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text

    # Delete profile
    profile_id = profile_data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_upload_file_invalid_format(client: TestClient, clean_db) -> None:
    """
    Test uploading an invalid file format (GIF).
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    profile_data = create_profile_with_invite(client, user_id, init_data)

    # Create test GIF image
    test_gif = create_test_image(format="GIF")

    # Try to upload GIF file
    files = {"file": ("test_image.gif", test_gif, "image/gif")}
    data = {"file_type": "avatar"}

    response = client.post(
        f"{settings.API_VERSION}/files/upload",
        files=files,
        data=data,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 400, response.text
    assert "Invalid file format" in response.json()["detail"]

    # Clean up
    profile_id = profile_data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_get_my_files(client: TestClient, clean_db) -> None:
    """
    Test getting user's files.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    profile_data = create_profile_with_invite(client, user_id, init_data)

    # Upload a test file
    test_image = create_test_image()
    files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
    data = {"file_type": "avatar"}

    upload_response = client.post(
        f"{settings.API_VERSION}/files/upload",
        files=files,
        data=data,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert upload_response.status_code == 200, upload_response.text

    # Get user's files
    response = client.get(
        f"{settings.API_VERSION}/files/",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    files_data = response.json()
    assert len(files_data) >= 1
    assert files_data[0]["type"] == "avatar"

    # Get files by type
    response = client.get(
        f"{settings.API_VERSION}/files/",
        params={"file_type": "avatar"},
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    files_data = response.json()
    assert len(files_data) >= 1
    assert all(file["type"] == "avatar" for file in files_data)

    # Clean up
    file_id = upload_response.json()["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text

    # Delete profile
    profile_id = profile_data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_get_file_by_id(client: TestClient, clean_db) -> None:
    """
    Test getting a specific file by ID.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    profile_data = create_profile_with_invite(client, user_id, init_data)

    # Upload a test file
    test_image = create_test_image()
    files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
    data = {"file_type": "avatar"}

    upload_response = client.post(
        f"{settings.API_VERSION}/files/upload",
        files=files,
        data=data,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert upload_response.status_code == 200, upload_response.text
    file_id = upload_response.json()["id"]

    # Get file by ID
    response = client.get(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 200, response.text
    file_data = response.json()
    assert file_data["id"] == file_id
    assert file_data["name"] == "test_image.jpg"
    assert file_data["type"] == "avatar"

    # Clean up
    resp = client.delete(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text

    # Delete profile
    profile_id = profile_data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_delete_file(client: TestClient, clean_db) -> None:
    """
    Test deleting a file.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # First, create a profile
    profile_data = create_profile_with_invite(client, user_id, init_data)

    # Upload a test file
    test_image = create_test_image()
    files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
    data = {"file_type": "avatar"}

    upload_response = client.post(
        f"{settings.API_VERSION}/files/upload",
        files=files,
        data=data,
        headers={"Authorization": f"tma {init_data}"},
    )
    assert upload_response.status_code == 200, upload_response.text
    file_id = upload_response.json()["id"]

    # Delete file
    response = client.delete(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 204, response.text

    # Try to get deleted file
    get_response = client.get(
        f"{settings.API_VERSION}/files/{file_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert get_response.status_code == 404, get_response.text

    # Delete profile
    profile_id = profile_data["id"]
    resp = client.delete(
        f"{settings.API_VERSION}/profiles/{profile_id}",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert resp.status_code == 204, response.text


# --------------------------------------------------------------------------------


def test_get_file_not_found(client: TestClient) -> None:
    """
    Test getting a non-existent file.
    Args:
        client (TestClient): FastAPI test client.
    Returns:
        None
    """
    # Create valid init data
    user_id = 123456789
    init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

    # Try to get non-existent file
    response = client.get(
        f"{settings.API_VERSION}/files/nonexistent-id",
        headers={"Authorization": f"tma {init_data}"},
    )
    assert response.status_code == 404, response.text
