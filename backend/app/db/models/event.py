import json
from uuid import uuid4

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class TagsType(TypeDecorator):
    """Custom type that handles tags as PostgreSQL arrays or JSON strings."""

    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(ARRAY(String))
        else:
            return dialect.type_descriptor(String)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if dialect.name == "postgresql":
            return value  # PostgreSQL handles arrays natively
        else:
            # For SQLite, store as JSON string
            return json.dumps(value) if value else None

    def process_result_value(self, value, dialect):
        if value is None:
            return []

        if dialect.name == "postgresql":
            return value if value else []  # PostgreSQL returns list directly
        else:
            # For SQLite, parse JSON string
            try:
                return json.loads(value) if value else []
            except (json.JSONDecodeError, TypeError):
                return []


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    photo = Column(String, ForeignKey("files.id"), nullable=True)
    tags = Column(TagsType, nullable=True)  # Compatible with both PostgreSQL and SQLite
    place = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    max_participants = Column(Integer, nullable=True)
    registration_start_date = Column(DateTime, nullable=True)
    registration_end_date = Column(DateTime, nullable=True)
    creator = Column(String, ForeignKey("profiles.id"), nullable=False)
    status = Column(String(1), nullable=False, default="A")  # A: ACTIVE, E: ENDED
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    creator_profile = relationship("Profile", viewonly=True)
    photo_file = relationship("File", foreign_keys=[photo], post_update=True, viewonly=True)
    participations = relationship(
        "EventParticipation", cascade="all, delete-orphan", lazy="select", viewonly=True
    )

    @property
    def photo_url(self) -> str | None:
        """Get the photo URL from the related file."""
        return self.photo_file.url if self.photo_file else None

    @property
    def participants_count(self) -> int:
        """Get the count of participants from participations table."""
        return len([p for p in self.participations if p.participation_type in ["C", "P"]])

    @property
    def participants(self) -> int:
        """Get the count of participants from participations table."""
        return self.participants_count

    @property
    def is_registration_available(self) -> bool:
        """Check if registration is currently available."""
        from datetime import datetime

        now = datetime.now()

        # Check registration dates
        if self.registration_start_date and now < self.registration_start_date:
            return False
        if self.registration_end_date and now > self.registration_end_date:
            return False

        # Check max participants
        if self.max_participants and self.participants_count >= self.max_participants:
            return False

        return True


class EventParticipation(Base):
    __tablename__ = "event_participations"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("profiles.id"), nullable=False, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False, index=True)
    participation_type = Column(String(1), nullable=False)  # C: CREATOR, P: PARTICIPANT, V: VIEWER
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("Profile", viewonly=True)
    event = relationship("Event", lazy="select", viewonly=True)
