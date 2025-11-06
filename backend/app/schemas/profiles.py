"""
Profile Schemas
Pydantic schemas for profile data validation and serialization.
"""

# --------------------------------------------------------------------------------

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

# --------------------------------------------------------------------------------


class ProfileBase(BaseModel):
    """
    Base schema for profile entity.

    Attributes:
        first_name (str): User's first name.
        last_name (str): User's last name.
        gender (str): User's gender (single character).
        birth_date (date): User's birth date.
        avatar (Optional[str]): ID of user's avatar file.
        university (str): User's university.
        bio (Optional[str]): User's biography.
        max_id (Optional[int]): User's Max ID.
        invited_by (Optional[str]): ID of the profile who invited this user.
    """

    first_name: str
    last_name: str
    gender: str
    birth_date: date
    avatar: Optional[str] = None
    university: str
    bio: Optional[str] = None
    max_id: Optional[int] = None
    invited_by: Optional[str] = None
    is_superuser: bool = False


# --------------------------------------------------------------------------------


class ProfilePatch(BaseModel):
    """
    Schema for patching a profile (partial update).
    Excludes protected fields: id, max_id, invited_by.

    Attributes:
        first_name (Optional[str]): User's first name.
        last_name (Optional[str]): User's last name.
        gender (Optional[str]): User's gender (single character).
        birth_date (Optional[date]): User's birth date.
        avatar (Optional[str]): ID of user's avatar file.
        university (Optional[str]): User's university.
        bio (Optional[str]): User's biography.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    avatar: Optional[str] = None
    university: Optional[str] = None
    bio: Optional[str] = None


class ProfileCreate(ProfilePatch):
    """
    Schema for creating a profile.
    Excludes protected fields: id, max_id, invited_by.

    Attributes:
        first_name (str): User's first name.
        last_name (str): User's last name.
        gender (str): User's gender (single character).
        birth_date (date): User's birth date.
        avatar (Optional[str]): ID of user's avatar file.
        university (str): User's university.
        bio (Optional[str]): User's biography.
    """

    first_name: str
    last_name: str
    gender: str
    birth_date: date
    avatar: Optional[str] = None
    university: str
    bio: Optional[str] = None


# --------------------------------------------------------------------------------


class ProfileInDBBase(ProfileBase):
    """
    Base schema for profile entity in DB.

    Attributes:
        id (str): Profile ID.
        created_at (datetime): Record creation timestamp.
    """

    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------------


class Profile(ProfileInDBBase):
    """
    Public schema for returning profile in API.
    Inherits all fields from ProfileInDBBase.

    Attributes:
        avatar_url (Optional[str]): URL to user's avatar file.
    """

    avatar_url: Optional[str] = None


# --------------------------------------------------------------------------------


class ProfileInDB(ProfileInDBBase):
    """
    Internal schema for profile entity in DB.
    Inherits all fields from ProfileInDBBase.
    """

    pass
