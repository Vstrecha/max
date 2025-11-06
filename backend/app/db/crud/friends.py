"""
Friends CRUD
CRUD operations for Friends model in the database.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.db.models import Friends, Profile

# --------------------------------------------------------------------------------


def create_friends(db: Session, user_1_id: str, user_2_id: str) -> Friends:
    """
    Create a new friends record in the database.

    Ensures user_1 < user_2 to maintain consistency.

    Args:
        db (Session): Database session.
        user_1_id (str): ID of the first user.
        user_2_id (str): ID of the second user.

    Returns:
        Friends: Created friends instance.
    """
    # Ensure user_1 < user_2 for consistency
    if user_1_id > user_2_id:
        user_1_id, user_2_id = user_2_id, user_1_id

    db_obj = Friends(
        id=str(uuid.uuid4()),
        user_1=user_1_id,
        user_2=user_2_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# --------------------------------------------------------------------------------


def get_friends_by_user(db: Session, user_id: str) -> list[Friends]:
    """
    Get all friends records for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        List[Friends]: List of friends records.
    """
    return db.query(Friends).filter((Friends.user_1 == user_id) | (Friends.user_2 == user_id)).all()


# --------------------------------------------------------------------------------


def get_friends_with_profiles(db: Session, user_id: str) -> list[tuple[Friends, Profile, Profile]]:
    """
    Get friends with profile information for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        List[Tuple[Friends, Profile, Profile]]: List of friends with profiles.
    """
    friends_records = (
        db.query(Friends)
        .options(joinedload(Friends.profile_1), joinedload(Friends.profile_2))
        .filter((Friends.user_1 == user_id) | (Friends.user_2 == user_id))
        .all()
    )

    result = []
    for friend_record in friends_records:
        if friend_record.user_1 == user_id:
            # Current user is user_1, friend is user_2
            current_user_profile = friend_record.profile_1
            friend_profile = friend_record.profile_2
        else:
            # Current user is user_2, friend is user_1
            current_user_profile = friend_record.profile_2
            friend_profile = friend_record.profile_1

        result.append((friend_record, current_user_profile, friend_profile))

    return result


# --------------------------------------------------------------------------------


def get_friends_of_friends_ids(db: Session, user_id: str) -> set[str]:
    """
    Get IDs of friends of friends (secondary friends) for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        Set[str]: Set of secondary friends IDs.
    """
    # Get direct friends
    direct_friends = get_friends_by_user(db, user_id)
    direct_friend_ids = set()

    for friend_record in direct_friends:
        if friend_record.user_1 == user_id:
            direct_friend_ids.add(friend_record.user_2)
        else:
            direct_friend_ids.add(friend_record.user_1)

    # Get secondary friends (friends of direct friends)
    secondary_friends = set()
    for friend_id in direct_friend_ids:
        friend_friends = get_friends_by_user(db, friend_id)
        for friend_friend_record in friend_friends:
            if friend_friend_record.user_1 == friend_id:
                secondary_friend_id = friend_friend_record.user_2
            else:
                secondary_friend_id = friend_friend_record.user_1

            # Don't include the original user or direct friends
            if secondary_friend_id != user_id and secondary_friend_id not in direct_friend_ids:
                secondary_friends.add(secondary_friend_id)

    return secondary_friends


def get_secondary_friends(db: Session, user_id: str) -> list[Profile]:
    """
    Get friends of friends (secondary friends) for a specific user.

    Args:
        db (Session): Database session.
        user_id (str): User ID.

    Returns:
        List[Profile]: List of secondary friends profiles.
    """
    secondary_friends_ids = get_friends_of_friends_ids(db, user_id)

    # Get profiles for secondary friends
    if secondary_friends_ids:
        return (
            db.query(Profile)
            .options(joinedload(Profile.avatar_file))
            .filter(Profile.id.in_(list(secondary_friends_ids)))
            .all()
        )

    return []


# --------------------------------------------------------------------------------


def delete_friends(db: Session, user_1_id: str, user_2_id: str) -> Optional[Friends]:
    """
    Delete a friends record between two users.

    Args:
        db (Session): Database session.
        user_1_id (str): ID of the first user.
        user_2_id (str): ID of the second user.

    Returns:
        Optional[Friends]: Deleted friends instance or None if not found.
    """
    # Ensure user_1 < user_2 for consistency
    if user_1_id > user_2_id:
        user_1_id, user_2_id = user_2_id, user_1_id

    friends_record = (
        db.query(Friends).filter(Friends.user_1 == user_1_id, Friends.user_2 == user_2_id).first()
    )

    if friends_record:
        db.delete(friends_record)
        db.commit()

    return friends_record


# --------------------------------------------------------------------------------


def are_friends(db: Session, user_1_id: str, user_2_id: str) -> bool:
    """
    Check if two users are friends.

    Args:
        db (Session): Database session.
        user_1_id (str): ID of the first user.
        user_2_id (str): ID of the second user.

    Returns:
        bool: True if users are friends, False otherwise.
    """
    # Ensure user_1 < user_2 for consistency
    if user_1_id > user_2_id:
        user_1_id, user_2_id = user_2_id, user_1_id

    friends_record = (
        db.query(Friends).filter(Friends.user_1 == user_1_id, Friends.user_2 == user_2_id).first()
    )

    return friends_record is not None


# --------------------------------------------------------------------------------


def delete_all_friends(db: Session) -> None:
    """
    Delete all friends records from the database.
    Used for testing purposes.

    Args:
        db (Session): Database session.
    """
    db.query(Friends).delete()
    db.commit()
