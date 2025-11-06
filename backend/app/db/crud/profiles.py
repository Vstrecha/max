"""
Profile CRUD
CRUD operations for Profile model in the database.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.db.models import Profile
from app.schemas.profiles import ProfileCreate, ProfilePatch

# --------------------------------------------------------------------------------


def create_profile(
    db: Session, obj_in: ProfileCreate, telegram: str, invited_by: Optional[str]
) -> Profile:
    """
    Create a new profile in the database.

    Args:
        db (Session): Database session.
        obj_in (ProfileCreate): Data for creating a profile.

    Returns:
        Profile: Created profile instance.
    """
    db_obj = Profile(
        id=str(uuid.uuid4()),
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        gender=obj_in.gender,
        birth_date=obj_in.birth_date,
        avatar=obj_in.avatar,
        university=obj_in.university,
        bio=obj_in.bio,
        telegram=telegram,
        invited_by=invited_by,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# --------------------------------------------------------------------------------


def get_profile_by_telegram(db: Session, telegram_id: int) -> Optional[Profile]:
    """
    Get a profile by Telegram ID.

    Args:
        db (Session): Database session.
        telegram_id (int): Telegram ID.

    Returns:
        Optional[Profile]: Profile instance or None if not found.
    """
    return (
        db.query(Profile)
        .options(joinedload(Profile.avatar_file))
        .filter(Profile.telegram == telegram_id)
        .first()
    )


# --------------------------------------------------------------------------------


def get_profile(db: Session, profile_id: str) -> Optional[Profile]:
    """
    Get a profile by ID.

    Args:
        db (Session): Database session.
        profile_id (str): Profile ID.

    Returns:
        Optional[Profile]: Profile instance or None if not found.
    """
    return (
        db.query(Profile)
        .options(joinedload(Profile.avatar_file))
        .filter(Profile.id == profile_id)
        .first()
    )


# --------------------------------------------------------------------------------


def get_profiles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Profile]:
    """
    Get a list of profiles with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Profile objects
    """
    return (
        db.query(Profile).options(joinedload(Profile.avatar_file)).offset(skip).limit(limit).all()
    )


# --------------------------------------------------------------------------------


def get_profiles_by_inviter(
    db: Session,
    inviter_id: str,
    skip: int = 0,
    limit: int = 100,
) -> list[Profile]:
    """
    Get a list of profiles invited by a specific profile.

    Args:
        db: Database session
        inviter_id: ID of the inviter profile
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Profile objects invited by the specified profile
    """
    return (
        db.query(Profile)
        .options(joinedload(Profile.avatar_file))
        .filter(Profile.invited_by == inviter_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# --------------------------------------------------------------------------------


def update_profile(db: Session, profile_id: str, obj_in: ProfilePatch) -> Optional[Profile]:
    """
    Update an existing profile in the database.

    Args:
        db (Session): Database session.
        profile_id (str): Profile ID.
        obj_in (ProfilePatch): Data for updating the profile.

    Returns:
        Optional[Profile]: Updated profile instance or None if not found.
    """
    db_obj = get_profile(db, profile_id=profile_id)
    if not db_obj:
        return None
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# --------------------------------------------------------------------------------


def remove_profile(db: Session, profile_id: str) -> Optional[Profile]:
    """
    Remove a profile from the database by ID.
    This will cascade delete all related records (files, events, invitations, etc.).
    """
    obj = db.query(Profile).filter(Profile.id == profile_id).first()
    if obj:
        # Note: Due to database constraints and business logic,
        # we typically don't allow profile deletion in production.
        # This function is mainly for testing purposes.
        # In production, consider soft deletion or deactivation instead.

        # The actual deletion will be handled by database cascade constraints
        # defined in the models (if configured properly)
        db.delete(obj)
        db.commit()
    return obj


# --------------------------------------------------------------------------------


def delete_all_profiles(db: Session) -> None:
    """
    Delete all profiles from the database.
    Used for testing purposes.

    Args:
        db (Session): Database session.
    """
    db.query(Profile).delete()
    db.commit()


# --------------------------------------------------------------------------------

# CRUD instance for easy import
profile = {
    "create": create_profile,
    "get": get_profile,
    "get_by_telegram": get_profile_by_telegram,
    "get_multi": get_profiles,
    "get_by_inviter": get_profiles_by_inviter,
    "update": update_profile,
    "remove": remove_profile,
    "delete_all": delete_all_profiles,
}
