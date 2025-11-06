"""
Friends Schemas
Pydantic schemas for friends data validation and serialization.
"""

# --------------------------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel

# --------------------------------------------------------------------------------


class FriendsBase(BaseModel):
    """
    Base schema for friends entity.

    Attributes:
        user_1 (str): ID of the first user.
        user_2 (str): ID of the second user.
    """

    user_1: str
    user_2: str


# --------------------------------------------------------------------------------


class FriendsCreate(BaseModel):
    """
    Schema for creating a new friends record.

    Attributes:
        user_1 (str): ID of the first user.
        user_2 (str): ID of the second user.
    """

    user_1: str
    user_2: str


# --------------------------------------------------------------------------------


class FriendsInDBBase(FriendsBase):
    """
    Base schema for friends entity in DB.

    Attributes:
        id (str): Friends record ID.
        created_at (datetime): Record creation timestamp.
    """

    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------------


class Friends(FriendsInDBBase):
    """
    Public schema for returning friends in API.
    Inherits all fields from FriendsInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class FriendsInDB(FriendsInDBBase):
    """
    Internal schema for friends entity in DB.
    Inherits all fields from FriendsInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class FriendsWithProfiles(BaseModel):
    """
    Schema for friends with profile information.

    Attributes:
        id (str): Friends record ID.
        user_1_profile (dict): First user's profile.
        user_2_profile (dict): Second user's profile.
        created_at (datetime): Record creation timestamp.
    """

    id: str
    user_1_profile: dict
    user_2_profile: dict
    created_at: datetime
