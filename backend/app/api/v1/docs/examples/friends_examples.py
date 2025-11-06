"""
Friends Examples
Example data for friends endpoints documentation.
"""

# --------------------------------------------------------------------------------

from .....core.config import settings

# --------------------------------------------------------------------------------

# GET /friends/my (get friends list)
get_friends_examples = {
    "examples": {
        "friends_list": {
            "summary": "Friends List",
            "description": "List of user's friends with profile information.",
            "value": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_1_profile": {
                        "id": "456e7890-e89b-12d3-a456-426614174001",
                        "first_name": "John",
                        "last_name": "Doe",
                        "gender": "M",
                        "birth_date": "1995-05-15",
                        "avatar": None,
                        "avatar_url": None,
                        "university": "HSE University",
                        "bio": "Software engineer.",
                        "telegram": 123456789,
                        "invited_by": None,
                        "created_at": "2024-07-01T12:00:00+00:00",
                    },
                    "user_2_profile": {
                        "id": "789e0123-e89b-12d3-a456-426614174002",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "gender": "F",
                        "birth_date": "1998-08-20",
                        "avatar": None,
                        "avatar_url": None,
                        "university": "Moscow State University",
                        "bio": "Data scientist.",
                        "telegram": 987654321,
                        "invited_by": None,
                        "created_at": "2024-07-01T13:00:00+00:00",
                    },
                    "created_at": "2024-07-01T14:00:00+00:00",
                }
            ],
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/friends/my"
response = requests.get(url, headers={{'Authorization': 'tma <init_data>'}})
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getFriends = async () => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/friends/my', {{
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error fetching friends:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# DELETE /friends/{profile_id} (delete friendship)
delete_friends_examples = {
    "examples": {
        "successful_delete": {
            "summary": "Successful Delete",
            "description": "Friendship deleted successfully.",
            "value": None,
        },
        "friendship_not_found": {
            "summary": "Friendship Not Found",
            "description": "Friendship between users does not exist.",
            "value": {"detail": "Friendship not found"},
        },
        "cannot_delete_self": {
            "summary": "Cannot Delete Self",
            "description": "Cannot delete friendship with yourself.",
            "value": {"detail": "Cannot delete friendship with yourself"},
        },
    },
    "responses": {
        204: {
            "description": "Friendship Deleted",
            "content": {"application/json": {"example": None}},
        },
        404: {
            "description": "Friendship Not Found",
            "content": {"application/json": {"example": {"detail": "Friendship not found"}}},
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"detail": "Cannot delete friendship with yourself"}
                }
            },
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

profile_id = "789e0123-e89b-12d3-a456-426614174002"
url = f"{settings.BASE_API_URL}/friends/{{profile_id}}"
response = requests.delete(url, headers={{'Authorization': 'tma <init_data>'}})
print(response.status_code)
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const deleteFriendship = async (profileId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/friends/${{profileId}}`, {{
      method: 'DELETE',
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    if (response.status === 204) {{
      console.log('Friendship deleted successfully');
      return true;
    }} else {{
      const data = await response.json();
      throw new Error(data.detail || 'Failed to delete friendship');
    }}
  }} catch (error) {{
    console.error('Error deleting friendship:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /friends/secondary (get secondary friends)
get_secondary_friends_examples = {
    "examples": {
        "secondary_friends_list": {
            "summary": "Secondary Friends List",
            "description": "List of friends of friends (secondary friends).",
            "value": [
                {
                    "id": "abc123-e89b-12d3-a456-426614174003",
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "gender": "F",
                    "birth_date": "1992-03-10",
                    "avatar": None,
                    "avatar_url": None,
                    "university": "Moscow Institute of Physics and Technology",
                    "bio": "Physicist.",
                    "telegram": 555666777,
                    "invited_by": None,
                    "created_at": "2024-07-01T15:00:00+00:00",
                }
            ],
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/friends/secondary"
response = requests.get(url, headers={{'Authorization': 'tma <init_data>'}})
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getSecondaryFriends = async () => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/friends/secondary', {{
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error fetching secondary friends:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /friends/new (create or get invitation)
create_invitation_examples = {
    "examples": {
        "invitation_created": {
            "summary": "Invitation Created",
            "description": "New invitation created or existing one retrieved.",
            "value": {
                "id": "inv123-e89b-12d3-a456-426614174004",
                "message": "Invitation created or retrieved successfully",
            },
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/friends/new"
response = requests.get(url, headers={{'Authorization': 'tma <init_data>'}})
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const createInvitation = async () => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/friends/new', {{
      method: 'GET',
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error creating invitation:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /friends/check/{invitation_id} (check invitation)
check_invitation_examples = {
    "examples": {
        "valid_invitation": {
            "summary": "Valid Invitation",
            "description": "Invitation exists and is valid.",
            "value": {
                "id": "inv123-e89b-12d3-a456-426614174004",
                "message": "Valid invitation",
            },
        },
        "invalid_invitation": {
            "summary": "Invalid Invitation",
            "description": "Invitation does not exist.",
            "value": {"detail": "INVALID_INVITATION"},
        },
    },
    "responses": {
        200: {
            "description": "Valid Invitation",
            "content": {
                "application/json": {"example": {"id": "inv123...", "message": "Valid invitation"}}
            },
        },
        404: {
            "description": "Invalid Invitation",
            "content": {"application/json": {"example": {"detail": "INVALID_INVITATION"}}},
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

invitation_id = "inv123-e89b-12d3-a456-426614174004"
url = f"{settings.BASE_API_URL}/friends/check/{{invitation_id}}"
response = requests.get(url, headers={{'Authorization': 'tma <init_data>'}})
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const checkInvitation = async (invitationId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/friends/check/${{invitationId}}`, {{
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error checking invitation:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# POST /friends/new (create friendship from invitation)
create_friends_examples = {
    "examples": {
        "friendship_created": {
            "summary": "Friendship Created",
            "description": "Friendship created successfully using invitation.",
            "value": {
                "id": "inv123-e89b-12d3-a456-426614174004",
                "message": "Friendship created successfully",
            },
        },
        "invalid_invitation": {
            "summary": "Invalid Invitation",
            "description": "Invitation ID is invalid.",
            "value": {"detail": "INVALID_INVITATION"},
        },
        "already_friends": {
            "summary": "Already Friends",
            "description": "Users are already friends.",
            "value": {"detail": "Already friends"},
        },
        "cannot_friend_self": {
            "summary": "Cannot Friend Self",
            "description": "Cannot become friends with yourself.",
            "value": {"detail": "Cannot become friends with yourself"},
        },
    },
    "responses": {
        200: {
            "description": "Friendship Created",
            "content": {
                "application/json": {
                    "example": {"id": "inv123...", "message": "Friendship created successfully"}
                }
            },
        },
        404: {
            "description": "Invalid Invitation",
            "content": {"application/json": {"example": {"detail": "INVALID_INVITATION"}}},
        },
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": "Already friends"}}},
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/friends/new"
data = {{"invitation_id": "inv123-e89b-12d3-a456-426614174004"}}
response = requests.post(url, json=data, headers={{'Authorization': 'tma <init_data>'}})
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const createFriendship = async (invitationId) => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/friends/new', {{
      method: 'POST',
      headers: {{
        'Authorization': 'tma <init_data>',
        'Content-Type': 'application/json'
      }},
      body: JSON.stringify({{ invitation_id: invitationId }})
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error creating friendship:', error);
    throw error;
  }}
}};
""",
        },
    ],
}
