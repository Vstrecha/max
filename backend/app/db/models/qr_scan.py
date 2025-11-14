"""
QR Scan Model
SQLAlchemy model for QR code scans entity and table definition.
"""

# --------------------------------------------------------------------------------

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

# --------------------------------------------------------------------------------


class QRScan(Base):
    """
    SQLAlchemy model for QR code scans.

    Attributes:
        id (str): Primary key (UUID as string).
        participation_id (str): ID of the event participation record.
        scanned_by_user_id (int): Max ID of the user who scanned the QR code.
        scanned_at (datetime): Timestamp when the QR code was scanned.
    """

    __tablename__ = "qr_scans"

    id = Column(String, primary_key=True, index=True)
    participation_id = Column(
        String, ForeignKey("event_participations.id"), nullable=False, index=True
    )
    scanned_by_user_id = Column(BigInteger, nullable=False, index=True)  # Max user ID
    scanned_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    participation = relationship("EventParticipation", viewonly=True)

    def __repr__(self):
        """
        Return a string representation of the QR scan.

        Returns:
            str: Human-readable representation of the QR scan.
        """
        return (
            f"<QRScan {self.id} - Participation: {self.participation_id}, "
            f"Scanned by: {self.scanned_by_user_id}>"
        )
