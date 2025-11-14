"""
QR Scan Schemas
Pydantic schemas for QR scan data validation and serialization.
"""

# --------------------------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel, ConfigDict

# --------------------------------------------------------------------------------


class QRScanCreate(BaseModel):
    """
    Schema for creating a QR scan.

    Attributes:
        participation_id (str): ID of the event participation record.
    """

    participation_id: str


class QRScanResponse(BaseModel):
    """
    Schema for QR scan response.

    Attributes:
        user_id (str): ID of the user who is registered for the event.
        event_id (str): ID of the event.
    """

    user_id: str
    event_id: str

    model_config = ConfigDict(from_attributes=True)


class QRScan(BaseModel):
    """
    Schema for QR scan entity.

    Attributes:
        id (str): QR scan ID.
        participation_id (str): ID of the event participation record.
        scanned_by_user_id (int): Max ID of the user who scanned the QR code.
        scanned_at (datetime): Timestamp when the QR code was scanned.
    """

    id: str
    participation_id: str
    scanned_by_user_id: int
    scanned_at: datetime

    model_config = ConfigDict(from_attributes=True)
