"""
Profile Model
SQLAlchemy model for profile entity and table definition.
"""

# --------------------------------------------------------------------------------


from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# --------------------------------------------------------------------------------


class Profile(Base):
    """
    SQLAlchemy model for profiles.

    Attributes:
        id (str): Primary key (UUID as string).
        first_name (str): User's first name.
        last_name (str): User's last name.
        gender (str): User's gender (single character).
        birth_date (date): User's birth date.
        avatar (str): ID of user's avatar file.
        university (str): User's university.
        bio (str): User's biography.
        max_id (int): User's Max ID.
        invited_by (str): ID of the profile who invited this user.
        created_at (datetime): Record creation timestamp.
    """

    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String(1), nullable=True)
    birth_date = Column(Date, nullable=True)
    avatar = Column(String, ForeignKey("files.id"), nullable=True)
    university = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    max_id = Column(BigInteger, nullable=False, index=True)
    invited_by = Column(String, ForeignKey("profiles.id"), nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationship to self for invited_by
    inviter = relationship("Profile", remote_side=[id], backref="invited_users")

    # Relationship to avatar file
    avatar_file = relationship("File", foreign_keys=[avatar], post_update=True)

    # Relationships to events
    created_events = relationship("Event", foreign_keys="Event.creator", viewonly=True)
    event_participations = relationship("EventParticipation", viewonly=True)

    def __repr__(self):
        """
        Return a string representation of the profile.

        Returns:
            str: Human-readable representation of the profile.
        """
        return f"<Profile {self.id} - {self.first_name} {self.last_name}>"
