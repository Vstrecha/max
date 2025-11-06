"""
File Examples
Example data for file endpoints documentation.
"""

# --------------------------------------------------------------------------------

from .....core.config import settings

# --------------------------------------------------------------------------------

# POST /files/upload (upload file)
upload_file_examples = {
    "examples": {
        "successful_upload": {
            "summary": "Successful Upload",
            "description": "File uploaded successfully.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "url": "https://storage.example.com/avatars/123e4567-e89b-12d3-a456-426614174000.webp",
            },
        },
        "invalid_file_format": {
            "summary": "Invalid File Format",
            "description": "GIF files are not allowed.",
            "value": {"detail": "Invalid file format. Only images (not GIF) are allowed."},
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

url = "{settings.BASE_API_URL}/files/upload"
files = {{"file": open("profile_photo.jpg", "rb")}}
data = {{"file_type": "avatar"}}
response = requests.post(url, files=files, data=data)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const uploadFile = async (file, fileType = 'avatar') => {{
  try {{
    const formData = new FormData();
    formData.append('file', file);
    formData.append('file_type', fileType);

    const response = await fetch('{settings.BASE_API_URL}/files/upload', {{
      method: 'POST',
      headers: {{ 'Authorization': 'tma <init_data>' }},
      body: formData
    }});
    const data = await response.json();
    console.log(data);
    if (!response.ok) {{
      throw new Error(data.detail || 'Failed to upload file');
    }}
    return data;
  }} catch (error) {{
    console.error('Error uploading file:', error);
    throw error;
  }}
}};
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /files/ (get my files)
get_my_files_examples = {
    "examples": {
        "files_list": {
            "summary": "Files List",
            "description": "List of user's files.",
            "value": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "profile_photo.jpg",
                    "url": "https://storage.example.com/avatars/123e4567-e89b-12d3-a456-426614174000.webp",
                    "user_id": "456e7890-e89b-12d3-a456-426614174001",
                    "type": "avatar",
                    "created_at": "2024-07-01T12:00:00+00:00",
                },
                {
                    "id": "789e0123-e89b-12d3-a456-426614174002",
                    "name": "event_photo.png",
                    "url": "https://storage.example.com/avatars/789e0123-e89b-12d3-a456-426614174002.webp",
                    "user_id": "456e7890-e89b-12d3-a456-426614174001",
                    "type": "event",
                    "created_at": "2024-07-01T13:00:00+00:00",
                },
            ],
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

# Get all files
url = "{settings.BASE_API_URL}/files/"
response = requests.get(url)
print(response.json())

# Get files by type
url = "{settings.BASE_API_URL}/files/"
params = {{"file_type": "avatar"}}
response = requests.get(url, params=params)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getMyFiles = async (fileType = null) => {{
  try {{
    const params = new URLSearchParams();
    if (fileType) {{
      params.append('file_type', fileType);
    }}
    const response = await fetch(`{settings.BASE_API_URL}/files/?${{params}}`, {{
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    return data;
  }} catch (error) {{
    console.error('Error fetching files:', error);
    throw error;
  }}
}};

// Usage: getMyFiles('avatar')
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# GET /files/{file_id} (get file by id)
get_file_examples = {
    "examples": {
        "file_found": {
            "summary": "File Found",
            "description": "File found by ID.",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "profile_photo.jpg",
                "url": "https://storage.example.com/avatars/123e4567-e89b-12d3-a456-426614174000.webp",
                "user_id": "456e7890-e89b-12d3-a456-426614174001",
                "type": "avatar",
                "created_at": "2024-07-01T12:00:00+00:00",
            },
        },
        "not_found": {
            "summary": "File Not Found",
            "description": "File with given ID does not exist.",
            "value": {"detail": "File not found"},
        },
        "forbidden": {
            "summary": "Access Forbidden",
            "description": "User can only access their own files.",
            "value": {"detail": "You can only access your own files"},
        },
    },
    "responses": {
        404: {
            "description": "File Not Found",
            "content": {"application/json": {"example": {"detail": "File not found"}}},
        },
        403: {
            "description": "Access Forbidden",
            "content": {
                "application/json": {"example": {"detail": "You can only access your own files"}}
            },
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

file_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"{settings.BASE_API_URL}/files/{{file_id}}"
response = requests.get(url)
print(response.json())
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const getFile = async (fileId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/files/${{fileId}}`, {{
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    const data = await response.json();
    if (!response.ok) {{
      throw new Error(data.detail || 'File not found');
    }}
    return data;
  }} catch (error) {{
    console.error('Error fetching file:', error);
    throw error;
  }}
}};

// Usage: getFile("123e4567-e89b-12d3-a456-426614174000")
""",
        },
    ],
}

# --------------------------------------------------------------------------------

# DELETE /files/{file_id} (delete file)
delete_file_examples = {
    "examples": {
        "successful_delete": {
            "summary": "Successful Delete",
            "description": "File deleted successfully.",
            "value": None,
        },
        "not_found": {
            "summary": "File Not Found",
            "description": "File with given ID does not exist.",
            "value": {"detail": "File not found"},
        },
        "forbidden": {
            "summary": "Access Forbidden",
            "description": "User can only delete their own files.",
            "value": {"detail": "You can only delete your own files"},
        },
    },
    "responses": {
        404: {
            "description": "File Not Found",
            "content": {"application/json": {"example": {"detail": "File not found"}}},
        },
        403: {
            "description": "Access Forbidden",
            "content": {
                "application/json": {"example": {"detail": "You can only delete your own files"}}
            },
        },
    },
    "x-code-samples": [
        {
            "lang": "Python",
            "source": f"""
import requests

file_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"{settings.BASE_API_URL}/files/{{file_id}}"
response = requests.delete(url)
print(response.status_code)
""",
        },
        {
            "lang": "Vue.js",
            "source": f"""
const deleteFile = async (fileId) => {{
  try {{
    const response = await fetch(`{settings.BASE_API_URL}/files/${{fileId}}`, {{
      method: 'DELETE',
      headers: {{ 'Authorization': 'tma <init_data>' }}
    }});
    if (response.status === 204) {{
      console.log('File deleted successfully');
      return true;
    }} else {{
      const data = await response.json();
      throw new Error(data.detail || 'File not found');
    }}
  }} catch (error) {{
    console.error('Error deleting file:', error);
    throw error;
  }}
}};

// Usage: deleteFile("123e4567-e89b-12d3-a456-426614174000")
""",
        },
    ],
}
