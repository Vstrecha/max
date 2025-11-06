"""
File Model
SQLAlchemy model for file entity and table definition.
"""

# --------------------------------------------------------------------------------

from enum import Enum

from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.sql import func

from app.db.base_class import Base

# --------------------------------------------------------------------------------


class FileType(str, Enum):
    """File type enumeration."""

    AVATAR = "avatar"
    EVENT = "event"


# --------------------------------------------------------------------------------


class File(Base):
    """
    SQLAlchemy model for files.

    Attributes:
        id (str): Primary key (UUID as string).
        name (str): Original file name.
        url (str): Public URL to the file in S3.
        max_id (int): Max ID of the user who uploaded the file.
        type (FileType): Type of file (avatar/event).
        created_at (datetime): Record creation timestamp.
    """

    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    max_id = Column(BigInteger, nullable=False, index=True)
    type = Column(String, nullable=False)  # FileType enum
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the file.

        Returns:
            str: Human-readable representation of the file.
        """
        return f"<File {self.id} - {self.name} ({self.type})>"
