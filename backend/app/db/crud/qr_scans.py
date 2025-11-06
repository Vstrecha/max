"""
QR Scan CRUD
CRUD operations for QRScan model in the database.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.qr_scan import QRScan

# --------------------------------------------------------------------------------


def create_qr_scan(db: Session, participation_id: str, scanned_by_user_id: int) -> QRScan:
    """
    Create a new QR scan record.

    Args:
        db (Session): Database session.
        participation_id (str): ID of the event participation record.
        scanned_by_user_id (int): Telegram ID of the user who scanned the QR code.

    Returns:
        QRScan: Created QR scan instance.
    """
    db_obj = QRScan(
        id=str(uuid.uuid4()),
        participation_id=participation_id,
        scanned_by_user_id=scanned_by_user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_qr_scan(db: Session, scan_id: str) -> Optional[QRScan]:
    """
    Get a QR scan by ID.

    Args:
        db (Session): Database session.
        scan_id (str): QR scan ID.

    Returns:
        Optional[QRScan]: QR scan instance or None if not found.
    """
    return db.query(QRScan).filter(QRScan.id == scan_id).first()


def get_qr_scans_by_participation(db: Session, participation_id: str) -> list[QRScan]:
    """
    Get all QR scans for a specific participation.

    Args:
        db (Session): Database session.
        participation_id (str): Participation ID.

    Returns:
        list[QRScan]: List of QR scan instances.
    """
    return db.query(QRScan).filter(QRScan.participation_id == participation_id).all()
