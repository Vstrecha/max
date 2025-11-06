"""
Friends Endpoints
FastAPI route handlers for friends and invitations API.
"""

# --------------------------------------------------------------------------------


from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.crud import friends as crud_friends
from app.db.crud import invitations as crud_invitations
from app.db.crud import profiles as crud_profiles
from app.schemas.invitations import CreateFriendsRequest, InvitationResponse
from app.schemas.profiles import Profile

from ....api.v1.docs.examples.friends_examples import (
    check_invitation_examples,
    create_friends_examples,
    create_invitation_examples,
    delete_friends_examples,
    get_friends_examples,
    get_secondary_friends_examples,
)
from ....db.session import get_db

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


@router.get("/my", response_model=list[Profile], openapi_extra=get_friends_examples)
async def get_my_friends(request: Request, db: Session = Depends(get_db)):
    """
    Get current user's friends list.

    Args:
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        List[FriendsWithProfiles]: List of friends with profile information.
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    friends_with_profiles = crud_friends.get_friends_with_profiles(db, profile.id)

    # Return only the friend's profile (exclude self)
    friends_only: list[dict] = []
    for _friend_record, _current_user_profile, friend_profile in friends_with_profiles:
        friends_only.append(profile_with_avatar_url(friend_profile))

    return friends_only


@router.get("/list/{profile_id}", response_model=list[Profile])
async def get_friends(profile_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Get friends list of profile_id profile.

    Args:
        profile_id (str): id of profile
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        List[FriendsWithProfiles]: List of friends with profile information.
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get required profile by profile_id
    required_profile = crud_profiles.get_profile(db, profile_id)
    if not required_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Required profile not found"
        )

    friends_with_profiles = crud_friends.get_friends_with_profiles(db, required_profile.id)

    # Return only the friend's profile (exclude self)
    friends_only: list[dict] = []
    for _friend_record, _current_user_profile, friend_profile in friends_with_profiles:
        friends_only.append(profile_with_avatar_url(friend_profile))

    return friends_only


# --------------------------------------------------------------------------------


@router.get(
    "/secondary", response_model=list[Profile], openapi_extra=get_secondary_friends_examples
)
async def get_secondary_friends(request: Request, db: Session = Depends(get_db)):
    """
    Get current user's secondary friends (friends of friends).

    Args:
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        List[Profile]: List of secondary friends profiles.
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    secondary_friends = crud_friends.get_secondary_friends(db, profile.id)

    return [profile_with_avatar_url(friend) for friend in secondary_friends]


# --------------------------------------------------------------------------------


@router.delete(
    "/{profile_id}", status_code=status.HTTP_204_NO_CONTENT, openapi_extra=delete_friends_examples
)
async def delete_friends(profile_id: str, request: Request, db: Session = Depends(get_db)):
    """
    Delete friendship between current user and specified profile.

    Args:
        profile_id (str): ID of the profile to remove friendship with.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        None: Always returns 204 (success).
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if friendship exists
    if not crud_friends.are_friends(db, profile.id, profile_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")

    crud_friends.delete_friends(db, profile.id, profile_id)
    return None


# --------------------------------------------------------------------------------


@router.get("/new", response_model=InvitationResponse, openapi_extra=create_invitation_examples)
async def create_or_get_invitation(request: Request, db: Session = Depends(get_db)):
    """
    Create or get invitation for current user.

    Args:
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        InvitationResponse: Invitation information.
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    invitation = crud_invitations.get_or_create_invitation(db, profile.id)

    return InvitationResponse(id=invitation.id)


# --------------------------------------------------------------------------------


@router.get(
    "/check/{invitation_id}",
    response_model=Profile,
    openapi_extra=check_invitation_examples,
)
async def check_invitation(invitation_id: str, db: Session = Depends(get_db)):
    """
    Check if invitation exists and is valid.

    Args:
        invitation_id (str): Invitation ID to check.
        db (Session): Database session.

    Returns:
        Profile: profile of referrer.
    """
    invitation = crud_invitations.get_invitation_by_id(db, invitation_id)
    if not invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INVALID_INVITATION")

    referrer = crud_profiles.get_profile(db, invitation.user_id)
    if not referrer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_INVITATION")

    return profile_with_avatar_url(referrer)


# --------------------------------------------------------------------------------


@router.post("/new", response_model=InvitationResponse, openapi_extra=create_friends_examples)
async def create_friends_from_invitation(
    request_data: CreateFriendsRequest, request: Request, db: Session = Depends(get_db)
):
    """
    Create friendship using invitation.

    Args:
        request_data (CreateFriendsRequest): Request data with invitation ID.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        InvitationResponse: Success message.
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if invitation exists
    invitation = crud_invitations.get_invitation_by_id(db, request_data.invitation_id)
    if not invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="INVALID_INVITATION")

    # Check if trying to become friends with self
    if profile.id == invitation.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot become friends with yourself"
        )

    # Check if already friends
    if crud_friends.are_friends(db, profile.id, invitation.user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already friends")

    # Create friendship
    crud_friends.create_friends(db, profile.id, invitation.user_id)

    return InvitationResponse(id=request_data.invitation_id)
