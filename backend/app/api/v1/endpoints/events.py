from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.config import ALL_TAGS
from app.db.crud import events as crud_events
from app.db.crud import profiles as crud_profiles
from app.db.crud import qr_scans as crud_qr_scans
from app.db.models.event import Event as EventModel
from app.db.models.event import EventParticipation
from app.db.session import get_db
from app.schemas.events import (
    Event,
    EventCreate,
    EventListResponse,
    EventUpdate,
    EventWithParticipation,
)
from app.schemas.qr_scans import QRScanCreate, QRScanResponse

router = APIRouter()


def _serialize_event(event_model: EventModel) -> Event:
    """Convert ORM event model to Pydantic schema."""
    return Event.model_validate(event_model, from_attributes=True)


def _serialize_event_with_participation(
    *,
    db: Session,
    event_model: EventModel,
    user_id: str,
) -> EventWithParticipation:
    """Convert ORM event model to response with participation info."""
    return EventWithParticipation(
        event=_serialize_event(event_model),
        friends_going=crud_events.event.get_friends_going_count(
            db, event_id=event_model.id, user_id=user_id
        ),
        friends_of_friends_going=crud_events.event.get_friends_of_friends_going_count(
            db, event_id=event_model.id, user_id=user_id
        ),
        participation_type=crud_events.event.get_user_participation_type(
            db, event_id=event_model.id, user_id=user_id
        ),
    )


@router.get(
    "/tags/",
    summary="Get all available event tags",
)
def get_available_tags():
    """
    Get all available event tags that can be used when creating or updating events.
    """
    return {"tags": ALL_TAGS}


@router.get(
    "/global_events/",
    response_model=EventListResponse,
    summary="Get global events with pagination and filtering",
)
def get_global_events(
    *,
    request: Request,
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    last_event_id: Optional[str] = Query(None),
    tags: Optional[list[str]] = Query(None),
):
    """
    Get global events with pagination and filtering.
    """
    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    events, total, has_more = crud_events.event.get_multi(
        db=db,
        limit=limit,
        last_event_id=last_event_id,
        tags=tags,
        user_id=user.id,
    )

    # Convert to EventWithParticipation format
    events_with_participation = [
        _serialize_event_with_participation(db=db, event_model=event, user_id=user.id)
        for event in events
    ]

    return EventListResponse(events=events_with_participation, total=total, has_more=has_more)


@router.get(
    "/global_events/{event_id}",
    response_model=EventWithParticipation,
    summary="Get event details with participation info",
)
def get_event_detail(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_id: str,
):
    """
    Get event details with participation information.
    """
    event = crud_events.event.get(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    # Create event dict with is_registration_available
    event_data = _serialize_event_with_participation(db=db, event_model=event, user_id=user.id)

    return event_data


@router.post(
    "/global_events/",
    response_model=Event,
    summary="Create a new event",
)
def create_event(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_in: EventCreate,
):
    """
    Create a new event.
    """
    current_user_id = request.state.user_id
    # Validate that the user exists
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    event = crud_events.event.create(db=db, obj_in=event_in, creator_id=user.id)
    return event


@router.patch(
    "/global_events/{event_id}",
    response_model=Event,
    summary="Update an event",
)
def update_event(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_id: str,
    event_in: EventUpdate,
):
    """
    Update an event. Only the creator can update the event.
    """
    event = crud_events.event.get(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    if not crud_events.event.is_creator(db, event_id=event_id, user_id=user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can update this event"
        )

    event = crud_events.event.update(db=db, db_obj=event, obj_in=event_in)
    return event


@router.delete("/global_events/{event_id}", summary="Delete an event")
def delete_event(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_id: str,
):
    """
    Delete an event. Only the creator can delete the event.
    """
    event = crud_events.event.get(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    if not crud_events.event.is_creator(db, event_id=event_id, user_id=user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can delete this event"
        )

    event = crud_events.event.delete(db=db, event_id=event_id)
    return event


@router.post(
    "/user_events/{event_id}",
    response_model=Event,
    summary="Register for an event",
)
def participate_in_event(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_id: str,
):
    """
    Register for an event. Users are automatically added as participants if they're
    not already participating.
    """
    # Validate that the event exists
    event = crud_events.event.get(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    # Check if user is the creator (creators cannot participate in their own events)
    if event.creator == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creators cannot participate in their own events",
        )

    # Check if registration is available
    if not event.is_registration_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is not available for this event",
        )

    # Add user participation (check if user is superuser)
    crud_events.event.participate_in_event(
        db, event_id=event_id, user_id=user.id, is_superuser=user.is_superuser
    )

    # Return event with is_registration_available
    return _serialize_event(event)


@router.delete("/user_events/{event_id}", summary="Leave an event")
def leave_event(
    *,
    request: Request,
    db: Session = Depends(get_db),
    event_id: str,
):
    """
    Leave an event. Users can leave events they're participating in.
    """
    # Validate that the event exists
    event = crud_events.event.get(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    # Check if user is the creator (creators cannot leave their own events)
    if event.creator == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Creators cannot leave their own events"
        )

    # Remove user participation
    success = crud_events.event.leave_event(db, event_id=event_id, user_id=user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not participating in this event"
        )

    return {"message": "Successfully left the event"}


@router.get(
    "/user_events/",
    response_model=EventListResponse,
    summary="Get user's events with filtering and pagination",
)
def get_user_events(
    *,
    request: Request,
    db: Session = Depends(get_db),
    filter_type: str = Query("all", pattern="^all|past|actual$"),
    limit: int = Query(20, ge=1, le=100),
    last_event_id: Optional[str] = Query(None),
):
    """
    Get user's events with filtering and pagination.
    """
    current_user_id = request.state.user_id
    # Validate that the user exists and get profile ID
    user = crud_profiles.get_profile_by_max_id(db, max_id=current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")

    # Get events where user is creator or participant
    from datetime import date

    from sqlalchemy import and_, or_

    from app.db.models.event import Event, EventParticipation

    query = (
        db.query(Event)
        .join(EventParticipation)
        .filter(
            or_(
                Event.creator == user.id,
                and_(
                    EventParticipation.event_id == Event.id,
                    EventParticipation.user_id == user.id,
                ),
            )
        )
        .distinct()
    )

    # Apply filters
    if filter_type == "past":
        query = query.filter(Event.end_date < date.today())
    elif filter_type == "actual":
        query = query.filter(Event.end_date >= date.today())

    # Apply pagination
    if last_event_id:
        last_event = db.query(Event).filter(Event.id == last_event_id).first()
        if last_event:
            query = query.filter(Event.created_at < last_event.created_at)

    # Get total count before pagination
    total = query.count()

    # Apply pagination - order by created_at desc for consistent pagination
    query = query.order_by(Event.created_at.desc()).limit(limit + 1)
    events = query.all()

    # Check if there are more events
    has_more = len(events) > limit
    if has_more:
        events = events[:-1]

    # Convert to EventWithParticipation format
    events_with_participation = [
        _serialize_event_with_participation(db=db, event_model=event, user_id=user.id)
        for event in events
    ]

    return EventListResponse(events=events_with_participation, total=total, has_more=has_more)


@router.post(
    "/scan_qr",
    response_model=QRScanResponse,
    summary="Scan QR code for event participation",
)
def scan_qr(
    *,
    request: Request,
    db: Session = Depends(get_db),
    scan_data: QRScanCreate,
):
    """
    Scan QR code for event participation.
    Creates a scan record and returns user_id and event_id.
    """
    current_user_id = request.state.user_id

    # Get participation record
    participation = (
        db.query(EventParticipation)
        .filter(EventParticipation.id == scan_data.participation_id)
        .first()
    )
    if not participation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participation not found")

    # Create QR scan record
    crud_qr_scans.create_qr_scan(
        db, participation_id=scan_data.participation_id, scanned_by_user_id=current_user_id
    )

    # Return user_id and event_id
    return QRScanResponse(user_id=participation.user_id, event_id=participation.event_id)
