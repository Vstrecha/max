"""
Friends Model
SQLAlchemy model for friends entity and table definition.
"""

# --------------------------------------------------------------------------------


from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# --------------------------------------------------------------------------------


class Friends(Base):
    """
    SQLAlchemy model for friends.

    Attributes:
        id (str): Primary key (UUID as string).
        user_1 (str): ID of the first user.
        user_2 (str): ID of the second user.
        created_at (datetime): Record creation timestamp.
    """

    __tablename__ = "friends"

    id = Column(String, primary_key=True, index=True)
    user_1 = Column(String, ForeignKey("profiles.id"), nullable=False, index=True)
    user_2 = Column(String, ForeignKey("profiles.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships to profiles
    profile_1 = relationship("Profile", foreign_keys=[user_1])
    profile_2 = relationship("Profile", foreign_keys=[user_2])

    # Ensure user_1 < user_2 to avoid duplicates
    __table_args__ = (UniqueConstraint("user_1", "user_2", name="uq_friends_users"),)

    def __repr__(self):
        """
        Return a string representation of the friends record.

        Returns:
            str: Human-readable representation of the friends record.
        """
        return f"<Friends {self.id} - {self.user_1} <-> {self.user_2}>"
