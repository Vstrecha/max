from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.config import ALL_TAGS


class BaseModelNoNulls(BaseModel):
    """Base model that removes None values from responses."""

    @staticmethod
    def _remove_none_recursive(obj):
        if isinstance(obj, dict):
            return {
                k: BaseModelNoNulls._remove_none_recursive(v)
                for k, v in obj.items()
                if v is not None
            }
        elif isinstance(obj, list):
            return [BaseModelNoNulls._remove_none_recursive(i) for i in obj if i is not None]
        return obj

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        return self._remove_none_recursive(data)


class EventBase(BaseModelNoNulls):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    photo: Optional[str] = None
    photo_url: Optional[str] = None
    tags: list[str] = Field(default_factory=list)  # Required but can be empty
    place: Optional[str] = None
    start_date: date
    end_date: date
    price: Optional[int] = Field(None, ge=0)
    visability: str = Field("G", pattern="^[GP]$")  # G: GLOBAL, P: PRIVATE
    repeatability: str = Field("N", pattern="^[NR]$")  # N: NONE, R: REPEATABLE
    status: str = Field("A", pattern="^[AE]$")  # A: ACTIVE, E: ENDED
    telegram_chat_link: Optional[str] = None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Validate that all tags are from the allowed list."""
        if v is None:
            return []
        for tag in v:
            if tag not in ALL_TAGS:
                raise ValueError(f"Tag '{tag}' is not allowed. Allowed tags: {ALL_TAGS}")
        return v


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, min_length=1)
    photo: Optional[str] = None
    tags: Optional[list[str]] = None
    place: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    price: Optional[int] = Field(None, ge=0)
    visability: Optional[str] = Field(None, pattern="^[GP]$")
    repeatability: Optional[str] = Field(None, pattern="^[NR]$")
    status: Optional[str] = Field(None, pattern="^[AE]$")
    telegram_chat_link: Optional[str] = None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Validate that all tags are from the allowed list."""
        if v is None:
            return None
        for tag in v:
            if tag not in ALL_TAGS:
                raise ValueError(f"Tag '{tag}' is not allowed. Allowed tags: {ALL_TAGS}")
        return v


class EventCreate(EventUpdate):
    # Required fields for creation
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    start_date: date
    end_date: date


class EventParticipationBase(BaseModel):
    participation_type: str = Field(..., pattern="^[CPV]$")  # C: CREATOR, P: PARTICIPANT, V: VIEWER


class EventParticipationCreate(EventParticipationBase):
    pass


class EventParticipation(EventParticipationBase):
    id: str
    user_id: str
    event_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Event(EventBase):
    id: str
    creator: str
    participants: int = Field(0, ge=0)  # Computed field for total participants
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class EventWithParticipation(BaseModel):
    event: Event
    friends_going: int = 0
    friends_of_friends_going: int = 0
    participation_type: str = "V"  # Default to VIEWER

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(BaseModel):
    events: list[EventWithParticipation]
    total: int
    has_more: bool
