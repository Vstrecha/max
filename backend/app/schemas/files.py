"""
File Schemas
Pydantic schemas for file data validation and serialization.
"""

# --------------------------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel

from app.db.models import FileType

# --------------------------------------------------------------------------------


class FileBase(BaseModel):
    """
    Base schema for file entity.

    Attributes:
        name (str): Original file name.
        url (str): Public URL to the file in S3.
        max_id (int): Max ID of the user who uploaded the file.
        type (FileType): Type of file (avatar/event).
    """

    name: str
    url: str
    max_id: int
    type: FileType


# --------------------------------------------------------------------------------


class FileCreate(BaseModel):
    """
    Schema for creating a new file.

    Attributes:
        name (str): Original file name.
        type (FileType): Type of file (avatar/event).
    """

    name: str
    type: FileType


# --------------------------------------------------------------------------------


class FileInDBBase(FileBase):
    """
    Base schema for file entity in DB.

    Attributes:
        id (str): File ID.
        created_at (datetime): Record creation timestamp.
    """

    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------------


class File(FileInDBBase):
    """
    Public schema for returning file in API.
    Inherits all fields from FileInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class FileInDB(FileInDBBase):
    """
    Internal schema for file entity in DB.
    Inherits all fields from FileInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class FileUploadResponse(BaseModel):
    """
    Response schema for file upload.

    Attributes:
        id (str): File ID.
        url (str): Public URL to the uploaded file.
    """

    id: str
    url: str
