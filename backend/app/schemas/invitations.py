"""
Invitations Schemas
Pydantic schemas for invitations data validation and serialization.
"""

# --------------------------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel

# --------------------------------------------------------------------------------


class InvitationsBase(BaseModel):
    """
    Base schema for invitations entity.

    Attributes:
        user_id (str): ID of the user who created the invitation.
    """

    user_id: str


# --------------------------------------------------------------------------------


class InvitationsCreate(BaseModel):
    """
    Schema for creating a new invitation.

    Attributes:
        user_id (str): ID of the user who created the invitation.
    """

    user_id: str


# --------------------------------------------------------------------------------


class InvitationsInDBBase(InvitationsBase):
    """
    Base schema for invitations entity in DB.

    Attributes:
        id (str): Invitation ID.
        created_at (datetime): Record creation timestamp.
    """

    id: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --------------------------------------------------------------------------------


class Invitations(InvitationsInDBBase):
    """
    Public schema for returning invitations in API.
    Inherits all fields from InvitationsInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class InvitationsInDB(InvitationsInDBBase):
    """
    Internal schema for invitations entity in DB.
    Inherits all fields from InvitationsInDBBase.
    """

    pass


# --------------------------------------------------------------------------------


class InvitationResponse(BaseModel):
    """
    Response schema for invitation operations.

    Attributes:
        id (str): Invitation ID.
    """

    id: str


# --------------------------------------------------------------------------------


class CreateFriendsRequest(BaseModel):
    """
    Request schema for creating friends from invitation.

    Attributes:
        invitation_id (str): ID of the invitation to use.
    """

    invitation_id: str
