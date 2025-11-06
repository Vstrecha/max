"""
Profile Examples
Example data for profile endpoints documentation.
"""

# --------------------------------------------------------------------------------

from .....core.config import settings

# --------------------------------------------------------------------------------

# POST /profiles/ (create profile)
create_profile_examples = {
    "examples": {
        "successful_creation": {
            "summary": "Successful Creation",
            "description": "Profile created successfully.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "birth_date": "1995-05-15",
                "avatar": None,
                "avatar_url": None,
                "university": "HSE University",
                "bio": "Software engineer with passion for technology.",
                "telegram": 123456789,
                "invited_by": None,
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "validation_error": {
            "summary": "Validation Error",
            "description": "Missing required fields.",
            "value": {
                "detail": [
                    {
                        "loc": ["body", "first_name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/profiles/"
data = {{
    "first_name": "John",
    "last_name": "Doe",
    "gender": "M",
    "birth_date": "1995-05-15",
    "photo_url": "https://example.com/photo.jpg",
    "university": "HSE University",
    "bio": "Software engineer with passion for technology.",
    "telegram": 123456789,
    "invited_by": None
}}
response = requests.post(url, json=data)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const createProfile = async (profile) => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/profiles/', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(profile)
    }});
    const data = await response.json();
    console.log(data);
    if (!response.ok) {{
      throw new Error(data.detail || 'Failed to create profile');
    }}
    return data;
  }} catch (error) {{
    console.error('Error creating profile:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /profiles/{profile_id} (get profile by id)
get_profile_examples = {
    "examples": {
        "profile_found": {
            "summary": "Profile Found",
            "description": "Profile found by ID.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "birth_date": "1995-05-15",
                "avatar": None,
                "avatar_url": None,
                "university": "HSE University",
                "bio": "Software engineer with passion for technology.",
                "telegram": 123456789,
                "invited_by": None,
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "not_found": {
            "summary": "Profile Not Found",
            "description": "Profile with given ID does not exist.",
            "value": {"detail": "Profile not found"},
        },
    },
    "responses": {
        404: {
            "description": "Profile Not Found",
            "content": {"application/json": {"example": {"detail": "Profile not found"}}},
        }
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

profile_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"{settings.BASE_API_URL}/profiles/{{profile_id}}"
response = requests.get(url)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getProfile = async (profileId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/profiles/${{profileId}}`);
    const data = await response.json();
    if (!response.ok) {{
      throw new Error(data.detail || 'Profile not found');
    }}
    return data;
  }} catch (error) {{
    console.error('Error fetching profile:', error);
    throw error;
  }}
}};

// Usage: getProfile("123e4567-e89b-12d3-a456-426614174000")
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# PUT /profiles/{profile_id} (update profile)
update_profile_examples = {
    "examples": {
        "successful_update": {
            "summary": "Successful Update",
            "description": "Profile updated successfully.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Smith",
                "gender": "M",
                "birth_date": "1995-05-15",
                "avatar": "456e7890-e89b-12d3-a456-426614174001",
                "avatar_url": "https://storage.example.com/avatars/456e7890-e89b-12d3-a456-426614174001.webp",
                "university": "HSE University",
                "bio": "Updated bio information.",
                "telegram": 123456789,
                "invited_by": None,
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "not_found": {
            "summary": "Profile Not Found",
            "description": "Profile with given ID does not exist.",
            "value": {"detail": "Profile not found"},
        },
    },
    "responses": {
        404: {
            "description": "Profile Not Found",
            "content": {"application/json": {"example": {"detail": "Profile not found"}}},
        }
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

profile_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"{settings.BASE_API_URL}/profiles/{{profile_id}}"
data = {{
    "last_name": "Smith",
    "photo_url": "https://example.com/new_photo.jpg",
    "bio": "Updated bio information."
}}
response = requests.put(url, json=data)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const updateProfile = async (profileId, profile) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/profiles/${{profileId}}`, {{
      method: 'PUT',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(profile)
    }});
    const data = await response.json();
    console.log(data);
    if (!response.ok) {{
      throw new Error(data.detail || 'Profile not found');
    }}
    return data;
  }} catch (error) {{
    console.error('Error updating profile:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# PATCH /profiles/ (patch profile)
patch_profile_examples = {
    "examples": {
        "successful_patch": {
            "summary": "Successful Patch",
            "description": "Profile patched successfully.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Smith",
                "gender": "M",
                "birth_date": "1995-05-15",
                "avatar": "456e7890-e89b-12d3-a456-426614174001",
                "avatar_url": "https://storage.example.com/avatars/456e7890-e89b-12d3-a456-426614174001.webp",
                "university": "HSE University",
                "bio": "Updated bio information.",
                "telegram": 123456789,
                "invited_by": None,
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "not_found": {
            "summary": "Profile Not Found",
            "description": "Profile with given Telegram ID does not exist.",
            "value": {"detail": "Profile not found"},
        },
    },
    "responses": {
        404: {
            "description": "Profile Not Found",
            "content": {"application/json": {"example": {"detail": "Profile not found"}}},
        }
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/profiles/"
data = {{
    "last_name": "Smith",
    "photo_url": "https://example.com/new_photo.jpg",
    "bio": "Updated bio information."
}}
response = requests.patch(url, json=data)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const patchProfile = async (profile) => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/profiles/', {{
      method: 'PATCH',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(profile)
    }});
    const data = await response.json();
    console.log(data);
    if (!response.ok) {{
      throw new Error(data.detail || 'Profile not found');
    }}
    return data;
  }} catch (error) {{
    console.error('Error patching profile:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /profiles/my (get current user's profile)
get_my_profile_examples = {
    "examples": {
        "my_profile_found": {
            "summary": "My Profile Found",
            "description": "Current user's profile found.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "birth_date": "1995-05-15",
                "avatar": None,
                "avatar_url": None,
                "university": "HSE University",
                "bio": "Software engineer with passion for technology.",
                "telegram": 123456789,
                "invited_by": None,
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "not_found": {
            "summary": "Profile Not Found",
            "description": "Current user's profile does not exist.",
            "value": {"detail": "Profile not found"},
        },
    },
    "responses": {
        404: {
            "description": "Profile Not Found",
            "content": {"application/json": {"example": {"detail": "Profile not found"}}},
        }
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/profiles/my"
response = requests.get(url)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getMyProfile = async () => {{
  try {{
    const response = await fetch('{settings.BASE_API_URL}/profiles/my');
    const data = await response.json();
    if (!response.ok) {{
      throw new Error(data.detail || 'Profile not found');
    }}
    return data;
  }} catch (error) {{
    console.error('Error fetching my profile:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# DELETE /profiles/{profile_id} (delete profile)
delete_profile_examples = {
    "examples": {
        "successful_delete": {
            "summary": "Successful Delete",
            "description": "Profile deleted successfully.",
            "value": None,
        },
        "not_found": {
            "summary": "Profile Not Found",
            "description": "Profile with given ID does not exist.",
            "value": {"detail": "Profile not found"},
        },
    },
    "responses": {
        404: {
            "description": "Profile Not Found",
            "content": {"application/json": {"example": {"detail": "Profile not found"}}},
        }
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

profile_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"{settings.BASE_API_URL}/profiles/{{profile_id}}"
response = requests.delete(url)
print(response.status_code)
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const deleteProfile = async (profileId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/profiles/${{profileId}}`, {{
      method: 'DELETE'
    }});
    if (response.status === 204) {{
      console.log('Profile deleted successfully');
      return true;
    }} else {{
      const data = await response.json();
      throw new Error(data.detail || 'Profile not found');
    }}
  }} catch (error) {{
    console.error('Error deleting profile:', error);
    throw error;
  }}
}};
""",
        },
    ],
}
