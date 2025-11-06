"""
Invitations Model
SQLAlchemy model for invitations entity and table definition.
"""

# --------------------------------------------------------------------------------


from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# --------------------------------------------------------------------------------


class Invitations(Base):
    """
    SQLAlchemy model for invitations.

    Attributes:
        id (str): Primary key (UUID as string).
        user_id (str): ID of the user who created the invitation.
        created_at (datetime): Record creation timestamp.
    """

    __tablename__ = "invitations"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationship to profile
    user = relationship("Profile", foreign_keys=[user_id])

    # Ensure only one invitation per user
    __table_args__ = (UniqueConstraint("user_id", name="uq_invitations_user"),)

    def __repr__(self):
        """
        Return a string representation of the invitation.

        Returns:
            str: Human-readable representation of the invitation.
        """
        return f"<Invitation {self.id} - User: {self.user_id}>"
