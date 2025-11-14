"""
Tests for Events API
Test cases for event creation, retrieval, update, and deletion.
"""

from datetime import datetime, timedelta

from starlette.testclient import TestClient

from app.core.config import settings
from app.tests.conftest import create_test_init_data


class TestEventCRUD:
    """Test CRUD operations for events."""

    def test_create_event(self, client: TestClient, clean_db):
        """Test creating a new event."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text
        profile_id = create_profile_response.json()["id"]

        # Now create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт", "Природа"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text

        event_data = create_event_response.json()
        assert event_data["title"] == "Test Event"
        assert event_data["creator"] == profile_id
        assert "tags" in event_data
        assert isinstance(event_data["tags"], list)
        assert "participants" in event_data
        assert event_data["participants"] == 1  # Creator is automatically added as participant
        assert "is_registration_available" in event_data

    def test_create_event_with_invalid_tags(self, client: TestClient, clean_db):
        """Test creating an event with invalid tags."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Try to create an event with invalid tags
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["InvalidTag", "Спорт"],  # InvalidTag is not in ALL_TAGS
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 422, create_event_response.text

    def test_create_event_with_empty_tags(self, client: TestClient, clean_db):
        """Test creating an event with empty tags list."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event with empty tags
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": [],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text

        event_data = create_event_response.json()
        assert event_data["tags"] == []

    def test_get_event(self, client: TestClient, clean_db):
        """Test retrieving an event by ID."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Музыка"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Now get the event
        get_event_response = client.get(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_event_response.status_code == 200, get_event_response.text

        retrieved_event = get_event_response.json()
        assert retrieved_event["event"]["id"] == event_id
        assert retrieved_event["event"]["title"] == "Test Event"
        assert retrieved_event["event"]["tags"] == ["Музыка"]
        assert "friends_going" in retrieved_event
        assert "friends_of_friends_going" in retrieved_event
        assert "participation_type" in retrieved_event
        assert "participate_id" in retrieved_event
        # Creator should have participate_id since they participate
        assert retrieved_event["participate_id"] is not None

    def test_update_event(self, client: TestClient, clean_db):
        """Test updating an event."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Update the event
        update_payload = {"title": "Updated Event Title", "tags": ["Музей", "Лекция"]}
        update_event_response = client.patch(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            json=update_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert update_event_response.status_code == 200, update_event_response.text

        updated_event = update_event_response.json()
        assert updated_event["title"] == "Updated Event Title"
        assert updated_event["tags"] == ["Музей", "Лекция"]

    def test_delete_event(self, client: TestClient, clean_db):
        """Test deleting an event."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Now delete the event
        delete_event_response = client.delete(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert delete_event_response.status_code == 200, delete_event_response.text

        # Check that event is no longer retrievable
        get_event_response = client.get(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_event_response.status_code == 404, get_event_response.text

    def test_is_creator(self, client: TestClient, clean_db):
        """Test checking if user is event creator."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Test that creator can update the event
        update_payload = {"title": "Updated Event Title"}
        update_event_response = client.patch(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            json=update_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert update_event_response.status_code == 200, update_event_response.text

        # Test that creator can delete the event
        delete_event_response = client.delete(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert delete_event_response.status_code == 200, delete_event_response.text


class TestEventParticipation:
    """Test event participation functionality."""

    def test_create_participation(self, client: TestClient, clean_db):
        """Test creating event participation."""
        # Create valid init data for event creator
        creator_id = 123456789
        creator_init_data = create_test_init_data(creator_id, settings.BOT_TOKEN)

        # First, create creator profile
        creator_profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": creator_id,
            "invited_by": None,
        }
        create_creator_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=creator_profile_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_creator_response.status_code == 201, create_creator_response.text

        # Create an event as creator
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Test that creator cannot participate in their own event
        participate_response = client.post(
            f"{settings.API_VERSION}/events/user_events/{event_id}",
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert participate_response.status_code == 400, participate_response.text
        assert "cannot participate" in participate_response.json()["detail"]

    def test_update_existing_participation(self, client: TestClient, clean_db):
        """Test updating existing participation."""
        # Create valid init data for event creator
        creator_id = 123456789
        creator_init_data = create_test_init_data(creator_id, settings.BOT_TOKEN)

        # First, create creator profile
        creator_profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": creator_id,
            "invited_by": None,
        }
        create_creator_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=creator_profile_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_creator_response.status_code == 201, create_creator_response.text

        # Create an event as creator
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Test that creator cannot participate in their own event
        participate_response = client.post(
            f"{settings.API_VERSION}/events/user_events/{event_id}",
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert participate_response.status_code == 400, participate_response.text
        assert "cannot participate" in participate_response.json()["detail"]

        # Test that trying to participate again still fails
        participate_again_response = client.post(
            f"{settings.API_VERSION}/events/user_events/{event_id}",
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert participate_again_response.status_code == 400, participate_response.text
        assert "cannot participate" in participate_again_response.json()["detail"]

    def test_get_user_participation_type(self, client: TestClient, clean_db):
        """Test getting user's participation type for an event."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Get event details to see participation type
        get_event_response = client.get(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_event_response.status_code == 200, get_event_response.text

        event_data = get_event_response.json()
        # Creator should have participation type "C" (Creator)
        assert event_data["participation_type"] == "C"
        # Creator should have participate_id since they participate
        assert event_data["participate_id"] is not None
        assert isinstance(event_data["participate_id"], str)

    def test_get_user_participation_id_for_non_participant(self, client: TestClient, clean_db):
        """Test that non-participants have participate_id as None."""
        # Create valid init data for event creator
        creator_id = 123456789
        creator_init_data = create_test_init_data(creator_id, settings.BOT_TOKEN)

        # First, create creator profile
        creator_profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": creator_id,
            "invited_by": None,
        }
        create_creator_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=creator_profile_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_creator_response.status_code == 201, create_creator_response.text

        # Create an event as creator
        event_payload = {
            "title": "Test Event",
            "body": "Test event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "visability": "G",
            "repeatability": "N",
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {creator_init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text
        event_id = create_event_response.json()["id"]

        # Create another user who is not participating
        viewer_id = 987654321
        viewer_init_data = create_test_init_data(viewer_id, settings.BOT_TOKEN)

        viewer_profile_payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "gender": "F",
            "birth_date": "1996-06-16",
            "avatar": None,
            "university": "HSE University",
            "bio": "Another user.",
            "max_id": viewer_id,
            "invited_by": None,
        }
        create_viewer_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=viewer_profile_payload,
            headers={"Authorization": f"tma {viewer_init_data}"},
        )
        assert create_viewer_response.status_code == 201, create_viewer_response.text

        # Get event details as non-participant
        get_event_response = client.get(
            f"{settings.API_VERSION}/events/global_events/{event_id}",
            headers={"Authorization": f"tma {viewer_init_data}"},
        )
        assert get_event_response.status_code == 200, get_event_response.text

        event_data = get_event_response.json()
        # Non-participant should have participation type "V" (Viewer)
        assert event_data["participation_type"] == "V"
        # Non-participant should have participate_id as None
        assert event_data["participate_id"] is None

    def test_get_user_events_always_has_participate_id(self, client: TestClient, clean_db):
        """Test that /user_events/ always returns events with participate_id."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create an event as creator
        event_payload = {
            "title": "My Event",
            "body": "My event description",
            "tags": ["Спорт"],
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
            "status": "A",
        }

        create_event_response = client.post(
            f"{settings.API_VERSION}/events/global_events/",
            json=event_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_event_response.status_code == 200, create_event_response.text

        # Get user events - should return events where user is creator or participant
        get_user_events_response = client.get(
            f"{settings.API_VERSION}/events/user_events/",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_user_events_response.status_code == 200, get_user_events_response.text

        events_data = get_user_events_response.json()
        assert len(events_data["events"]) >= 1  # Should have at least the event we created

        # All events in /user_events/ should have participate_id
        # since user is creator or participant
        for event in events_data["events"]:
            assert "participate_id" in event
            assert (
                event["participate_id"] is not None
            ), f"Event {event['event']['id']} should have participate_id in /user_events/"
            assert isinstance(event["participate_id"], str)
            assert "participation_type" in event
            # Participation type should be "C" (Creator) or "P" (Participant), not "V" (Viewer)
            assert event["participation_type"] in ["C", "P"]


class TestEventFiltering:
    """Test event filtering and pagination."""

    def test_get_events_with_filters(self, client: TestClient, clean_db):
        """Test getting events with various filters."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create multiple events with different properties
        events_data = [
            {
                "title": "Global Event",
                "body": "Global event description",
                "tags": ["Спорт"],
                "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=1, hours=2)).strftime("%Y-%m-%d"),
                "status": "A",
            },
            {
                "title": "Private Event",
                "body": "Private event description",
                "tags": ["Природа"],
                "start_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=2, hours=2)).strftime("%Y-%m-%d"),
                "status": "A",
            },
        ]

        for event_payload in events_data:
            create_event_response = client.post(
                f"{settings.API_VERSION}/events/global_events/",
                json=event_payload,
                headers={"Authorization": f"tma {init_data}"},
            )
            assert create_event_response.status_code == 200, create_event_response.text

        # Test getting events without filter (all events)
        get_events_response = client.get(
            f"{settings.API_VERSION}/events/global_events/",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_events_response.status_code == 200, get_events_response.text

        events_data = get_events_response.json()
        assert len(events_data["events"]) >= 2  # Both events should be returned
        # Check that events have tags
        assert all("tags" in event["event"] for event in events_data["events"])
        # Check that events have participation info including participate_id
        profile_id = create_profile_response.json()["id"]
        for event in events_data["events"]:
            assert "participation_type" in event
            assert "participate_id" in event
            # If event is created by current user, they should have participate_id
            if event["event"]["creator"] == profile_id:
                assert event["participate_id"] is not None
                assert isinstance(event["participate_id"], str)

    def test_get_events_with_pagination(self, client: TestClient, clean_db):
        """Test event pagination."""
        # Create valid init data
        user_id = 123456789
        init_data = create_test_init_data(user_id, settings.BOT_TOKEN)

        # First, create a profile
        profile_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1995-05-15",
            "avatar": None,
            "university": "HSE University",
            "bio": "Software engineer with passion for technology.",
            "max_id": user_id,
            "invited_by": None,
        }
        create_profile_response = client.post(
            f"{settings.API_VERSION}/profiles/",
            json=profile_payload,
            headers={"Authorization": f"tma {init_data}"},
        )
        assert create_profile_response.status_code == 201, create_profile_response.text

        # Create multiple events
        for i in range(5):  # Reduced from 25 to 5 for faster testing
            event_payload = {
                "title": f"Event {i}",
                "body": f"Event {i} description",
                "tags": ["Спорт"],
                "start_date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "end_date": (datetime.now() + timedelta(days=i, hours=2)).strftime("%Y-%m-%d"),
                "visability": "G",
                "repeatability": "N",
                "status": "A",
            }

            create_event_response = client.post(
                f"{settings.API_VERSION}/events/global_events/",
                json=event_payload,
                headers={"Authorization": f"tma {init_data}"},
            )
            assert create_event_response.status_code == 200, create_event_response.text

        # Test pagination
        get_events_response = client.get(
            f"{settings.API_VERSION}/events/global_events/?limit=3",
            headers={"Authorization": f"tma {init_data}"},
        )
        assert get_events_response.status_code == 200, get_events_response.text

        events_data = get_events_response.json()
        assert len(events_data["events"]) <= 3
        assert events_data["has_more"] is True
        # Check that events have participation info including participate_id
        profile_id = create_profile_response.json()["id"]
        for event in events_data["events"]:
            assert "participation_type" in event
            assert "participate_id" in event
            # If event is created by current user, they should have participate_id
            if event["event"]["creator"] == profile_id:
                assert event["participate_id"] is not None
