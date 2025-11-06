"""
Invitations CRUD
CRUD operations for Invitations model in the database.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Invitations

# --------------------------------------------------------------------------------


def create_invitation(db: Session, user_id: str) -> Invitations:
    """
    Create a new invitation for a user.

    Args:
        db (Session): Database session.
        user_id (str): ID of the user.

    Returns:
        Invitations: Created invitation instance.
    """
    db_obj = Invitations(
        id=str(uuid.uuid4()),
        user_id=user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# --------------------------------------------------------------------------------


def get_invitation_by_user(db: Session, user_id: str) -> Optional[Invitations]:
    """
    Get invitation for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        Optional[Invitations]: Invitation instance or None if not found.
    """
    return db.query(Invitations).filter(Invitations.user_id == user_id).first()


# --------------------------------------------------------------------------------


def get_or_create_invitation(db: Session, user_id: str) -> Invitations:
    """
    Get existing invitation for a user or create a new one.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        Invitations: Invitation instance.
    """
    invitation = get_invitation_by_user(db, user_id)
    if not invitation:
        invitation = create_invitation(db, user_id)
    return invitation


# --------------------------------------------------------------------------------


def get_invitation_by_id(db: Session, invitation_id: str) -> Optional[Invitations]:
    """
    Get invitation by ID.

    Args:
        db (Session): Database session.
        invitation_id (str): Invitation ID.

    Returns:
        Optional[Invitations]: Invitation instance or None if not found.
    """
    return db.query(Invitations).filter(Invitations.id == invitation_id).first()


# --------------------------------------------------------------------------------


def delete_invitation(db: Session, invitation_id: str) -> Optional[Invitations]:
    """
    Delete an invitation by ID.

    Args:
        db (Session): Database session.
        invitation_id (str): Invitation ID.

    Returns:
        Optional[Invitations]: Deleted invitation instance or None if not found.
    """
    invitation = get_invitation_by_id(db, invitation_id)
    if invitation:
        db.delete(invitation)
        db.commit()
    return invitation


# --------------------------------------------------------------------------------


def delete_invitation_by_user(db: Session, user_id: str) -> Optional[Invitations]:
    """
    Delete invitation for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        Optional[Invitations]: Deleted invitation instance or None if not found.
    """
    invitation = get_invitation_by_user(db, user_id)
    if invitation:
        db.delete(invitation)
        db.commit()
    return invitation


# --------------------------------------------------------------------------------


def delete_all_invitations(db: Session) -> None:
    """
    Delete all invitations from the database.
    Used for testing purposes.

    Args:
        db (Session): Database session.
    """
    db.query(Invitations).delete()
    db.commit()
