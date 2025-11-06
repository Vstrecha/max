"""
Schemas Package
Pydantic schemas for data validation and serialization.
"""

from .events import (
    Event,
    EventBase,
    EventCreate,
    EventListResponse,
    EventParticipation,
    EventParticipationBase,
    EventParticipationCreate,
    EventUpdate,
    EventWithParticipation,
)
from .files import File, FileBase, FileCreate, FileInDB, FileInDBBase, FileUploadResponse
from .friends import (
    Friends,
    FriendsBase,
    FriendsCreate,
    FriendsInDB,
    FriendsInDBBase,
    FriendsWithProfiles,
)
from .invitations import (
    CreateFriendsRequest,
    InvitationResponse,
    Invitations,
    InvitationsBase,
    InvitationsCreate,
    InvitationsInDB,
    InvitationsInDBBase,
)
from .profiles import (
    Profile,
    ProfileBase,
    ProfileCreate,
    ProfileInDB,
    ProfileInDBBase,
    ProfilePatch,
)

# --------------------------------------------------------------------------------

__all__ = [
    "ProfileBase",
    "ProfileCreate",
    "ProfilePatch",
    "ProfileInDBBase",
    "Profile",
    "ProfileInDB",
    "FileBase",
    "FileCreate",
    "FileInDBBase",
    "File",
    "FileInDB",
    "FileUploadResponse",
    "FriendsBase",
    "FriendsCreate",
    "FriendsInDBBase",
    "Friends",
    "FriendsInDB",
    "FriendsWithProfiles",
    "InvitationsBase",
    "InvitationsCreate",
    "InvitationsInDBBase",
    "Invitations",
    "InvitationsInDB",
    "InvitationResponse",
    "CreateFriendsRequest",
    "Event",
    "EventBase",
    "EventCreate",
    "EventUpdate",
    "EventWithParticipation",
    "EventListResponse",
    "EventParticipation",
    "EventParticipationCreate",
    "EventParticipationBase",
]
