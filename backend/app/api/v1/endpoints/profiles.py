"""
Profile Endpoints
FastAPI route handlers for profile entity API.
"""

# --------------------------------------------------------------------------------

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.db.crud import files as crud_files
from app.db.crud import friends as crud_friends
from app.db.crud import invitations as crud_invitations
from app.db.crud import profiles as crud_profiles

from ....api.v1.docs.examples.profile_examples import (
    create_profile_examples,
    delete_profile_examples,
    get_my_profile_examples,
    get_profile_examples,
    patch_profile_examples,
)
from ....db.session import get_db
from ....schemas.profiles import Profile, ProfileCreate, ProfilePatch

# --------------------------------------------------------------------------------

router = APIRouter()

# --------------------------------------------------------------------------------


def profile_with_avatar_url(profile) -> dict:
    """
    Convert profile to dict with avatar_url.

    Args:
        profile: Profile instance from database.

    Returns:
        dict: Profile data with avatar_url.
    """
    profile_dict = {
        "id": profile.id,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "gender": profile.gender,
        "birth_date": profile.birth_date,
        "avatar": profile.avatar,
        "university": profile.university,
        "bio": profile.bio,
        "telegram": profile.telegram,
        "invited_by": profile.invited_by,
        "created_at": profile.created_at,
        "avatar_url": profile.avatar_file.url if profile.avatar_file else None,
    }
    return profile_dict


# --------------------------------------------------------------------------------


@router.get("/my", response_model=Optional[Profile], openapi_extra=get_my_profile_examples)
async def read_my_profile(request: Request, db: Session = Depends(get_db)):
    """
    Get the current user's profile.

    Args:
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        Profile: Current user's profile schema.
    """
    user_id = request.state.user_id
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return profile_with_avatar_url(profile)


# --------------------------------------------------------------------------------


@router.get("/{profile_id}", response_model=Profile, openapi_extra=get_profile_examples)
async def read_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Get a profile by ID.

    Args:
        profile_id (str): Profile ID.
        db (Session): Database session.

    Returns:
        Profile: Profile schema.
    """
    profile = crud_profiles.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_with_avatar_url(profile)


# --------------------------------------------------------------------------------


@router.get("/{profile_id}/invited", response_model=list[Profile])
async def read_invited_profiles(
    profile_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get a list of profiles invited by a specific profile.

    Args:
        profile_id (str): Profile ID of the inviter.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): Database session.

    Returns:
        List[Profile]: List of invited profile schemas.
    """
    invited_profiles = crud_profiles.get_profiles_by_inviter(db, profile_id, skip=skip, limit=limit)
    return [profile_with_avatar_url(profile) for profile in invited_profiles]


# --------------------------------------------------------------------------------


@router.post(
    "/",
    response_model=Profile,
    status_code=status.HTTP_201_CREATED,
    openapi_extra=create_profile_examples,
)
async def create_profile(
    profile_in: ProfileCreate, request: Request, db: Session = Depends(get_db)
):
    """
    Create a new profile.

    Args:
        profile_in (ProfileCreate): Profile creation schema.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        Profile: Created profile schema.
    """
    user_id = request.state.user_id

    # Validate avatar file if provided
    if profile_in.avatar:
        avatar_file = crud_files.get_file(db, profile_in.avatar)
        if not avatar_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Avatar file not found"
            )

    # Check if this is the first user (no profiles exist yet)
    existing_profiles = crud_profiles.get_profiles(db, limit=1)

    if len(existing_profiles) == 0:
        # First user - no invitation required
        profile = crud_profiles.create_profile(db, profile_in, telegram=user_id, invited_by=None)
        return profile_with_avatar_url(profile)

    # Check if invitation exists and is valid
    if not profile_in.invitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation ID is required for new users",
        )

    invitation = crud_invitations.get_invitation_by_id(db, profile_in.invitation)
    if not invitation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid invitation ID")

    profile_by_tg = crud_profiles.get_profile_by_telegram(db, user_id)
    if profile_by_tg:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Profile already exists")

    profile = crud_profiles.create_profile(
        db, profile_in, telegram=user_id, invited_by=invitation.user_id
    )

    # Create friendship between the inviter and the new user
    crud_friends.create_friends(db, invitation.user_id, profile.id)

    return profile_with_avatar_url(profile)


# --------------------------------------------------------------------------------


@router.patch("/", response_model=Profile, openapi_extra=patch_profile_examples)
async def update_profile(profile_in: ProfilePatch, request: Request, db: Session = Depends(get_db)):
    """
    Update the current user's profile.

    Args:
        profile_in (ProfilePatch): Profile update schema.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        Profile: Updated profile schema.
    """
    user_id = request.state.user_id

    # Get profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Validate avatar file if provided
    if profile_in.avatar:
        avatar_file = crud_files.get_file(db, profile_in.avatar)
        if not avatar_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Avatar file not found"
            )

    updated_profile = crud_profiles.update_profile(db, profile.id, profile_in)
    return profile_with_avatar_url(updated_profile)


# --------------------------------------------------------------------------------


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    openapi_extra=delete_profile_examples,
)
async def delete_profile(profile_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Delete a profile by ID.

    Args:
        profile_id (str): Profile ID.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        None: Always returns 204 (success).
    """
    user_id = request.state.user_id

    # Get profile to check ownership
    profile = crud_profiles.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if user owns this profile
    if profile.telegram != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own profile"
        )

    crud_profiles.remove_profile(db, profile_id)
    return None
