from typing import Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.db.crud.friends import get_friends_of_friends_ids
from app.db.models.event import Event, EventParticipation
from app.db.models.friends import Friends
from app.schemas.events import EventCreate, EventUpdate


class CRUDEvent:
    def create(self, db: Session, *, obj_in: EventCreate, creator_id: str) -> Event:
        """Create a new event."""
        db_obj = Event(
            title=obj_in.title,
            body=obj_in.body,
            photo=obj_in.photo,
            place=obj_in.place,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            price=obj_in.price,
            creator=creator_id,
            visability=obj_in.visability,
            repeatability=obj_in.repeatability,
            status=obj_in.status,
            telegram_chat_link=obj_in.telegram_chat_link,
        )
        # Set tags directly as PostgreSQL array
        db_obj.tags = obj_in.tags if obj_in.tags is not None else []
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create creator participation record
        participation = EventParticipation(
            user_id=creator_id, event_id=db_obj.id, participation_type="C"
        )
        db.add(participation)
        db.commit()

        return db_obj

    def get(self, db: Session, event_id: str) -> Optional[Event]:
        """Get event by ID."""
        return db.query(Event).filter(Event.id == event_id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        last_event_id: Optional[str] = None,
        tags: Optional[list[str]] = None,
        visability: Optional[str] = None,
        repeatability: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[Event], int, bool]:
        """Get multiple events with filtering and pagination."""
        query = db.query(Event)

        # Apply cursor-based pagination
        if last_event_id:
            last_event = db.query(Event).filter(Event.id == last_event_id).first()
            if last_event:
                query = query.filter(Event.created_at < last_event.created_at)

        # Filter by tags - handle both PostgreSQL and SQLite
        if tags:
            # Check if we're using PostgreSQL or SQLite
            if db.bind.dialect.name == "postgresql":
                # For PostgreSQL, use array overlap operator
                query = query.filter(Event.tags.op("&&")(tags))
            else:
                # For SQLite, check if any tag exists in the JSON array
                tag_conditions = []
                for tag in tags:
                    tag_conditions.append(Event.tags.contains(f'"{tag}"'))
                if tag_conditions:
                    query = query.filter(or_(*tag_conditions))

        if visability:
            query = query.filter(Event.visability == visability)
        else:
            # If no visibility filter specified, show public events and private
            # events with friendship access
            if user_id:
                # Get user's friends
                friends_query = db.query(Friends).filter(
                    or_(Friends.user_1 == user_id, Friends.user_2 == user_id)
                )
                friend_ids = set()
                for friendship in friends_query.all():
                    if friendship.user_1 == user_id:
                        friend_ids.add(friendship.user_2)
                    else:
                        friend_ids.add(friendship.user_1)

                # Show public events OR private events where user is creator or
                # has friend participating
                query = query.filter(
                    or_(
                        Event.visability == "G",
                        and_(
                            Event.visability == "P",
                            or_(
                                Event.creator == user_id,
                                Event.id.in_(
                                    db.query(EventParticipation.event_id).filter(
                                        EventParticipation.user_id.in_(friend_ids)
                                    )
                                ),
                            ),
                        ),
                    )
                )
            else:
                # No user context, show only public events
                query = query.filter(Event.visability == "G")

        if repeatability:
            query = query.filter(Event.repeatability == repeatability)

        # Get total count before pagination
        total = query.count()

        # Apply pagination - order by created_at desc for consistent pagination
        query = query.order_by(Event.created_at.desc()).offset(skip).limit(limit + 1)
        events = query.all()

        # Check if there are more events
        has_more = len(events) > limit
        if has_more:
            events = events[:-1]

        return events, total, has_more

    def update(self, db: Session, *, db_obj: Event, obj_in: EventUpdate) -> Event:
        """Update an event."""
        update_data = obj_in.model_dump(exclude_unset=True)

        # Handle tags separately - set directly as PostgreSQL array
        if "tags" in update_data:
            db_obj.tags = update_data.pop("tags")

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, event_id: str) -> Event:
        """Delete an event."""
        obj = db.get(Event, event_id)
        db.delete(obj)
        db.commit()
        return obj

    def is_creator(self, db: Session, *, event_id: str, user_id: str) -> bool:
        """Check if user is the creator of the event."""
        event = db.query(Event).filter(Event.id == event_id).first()
        return event and event.creator == user_id

    def get_user_participation_type(self, db: Session, *, event_id: str, user_id: str) -> str:
        """
        Get user's participation type for an event. Returns 'V' (VIEWER) if no
        participation found.
        """
        participation = (
            db.query(EventParticipation)
            .filter(
                and_(EventParticipation.event_id == event_id, EventParticipation.user_id == user_id)
            )
            .first()
        )
        return participation.participation_type if participation else "V"

    def get_friends_going_count(self, db: Session, *, event_id: str, user_id: str) -> int:
        """Get count of friends going to the event."""
        # Get user's friends
        friends_query = db.query(Friends).filter(
            or_(Friends.user_1 == user_id, Friends.user_2 == user_id)
        )
        friend_ids = set()
        for friendship in friends_query.all():
            if friendship.user_1 == user_id:
                friend_ids.add(friendship.user_2)
            else:
                friend_ids.add(friendship.user_1)

        if not friend_ids:
            return 0

        # Count friends participating in the event
        friends_participating = (
            db.query(EventParticipation)
            .filter(
                and_(
                    EventParticipation.event_id == event_id,
                    EventParticipation.user_id.in_(friend_ids),
                    EventParticipation.participation_type.in_(["C", "P"]),
                )
            )
            .count()
        )

        return friends_participating

    def get_friends_of_friends_going_count(
        self, db: Session, *, event_id: str, user_id: str
    ) -> int:
        """Get count of friends of friends going to the event."""
        # Get friends of friends IDs
        friends_of_friends_ids = get_friends_of_friends_ids(db, user_id=user_id)

        if not friends_of_friends_ids:
            return 0

        # Count friends of friends participating in the event
        friends_of_friends_participating = (
            db.query(EventParticipation)
            .filter(
                and_(
                    EventParticipation.event_id == event_id,
                    EventParticipation.user_id.in_(friends_of_friends_ids),
                    EventParticipation.participation_type.in_(["C", "P"]),
                )
            )
            .count()
        )

        return friends_of_friends_participating

    def participate_in_event(
        self, db: Session, *, event_id: str, user_id: str, participation_type: str = "P"
    ) -> EventParticipation:
        """Add user participation to an event."""
        # Check if participation already exists
        existing_participation = (
            db.query(EventParticipation)
            .filter(
                and_(EventParticipation.event_id == event_id, EventParticipation.user_id == user_id)
            )
            .first()
        )

        if existing_participation:
            # Update existing participation
            existing_participation.participation_type = participation_type
            db.add(existing_participation)
            db.commit()
            db.refresh(existing_participation)
            return existing_participation
        else:
            # Create new participation
            participation = EventParticipation(
                user_id=user_id, event_id=event_id, participation_type=participation_type
            )
            db.add(participation)
            db.commit()
            db.refresh(participation)
            return participation

    def leave_event(self, db: Session, *, event_id: str, user_id: str) -> bool:
        """Remove user participation from an event."""
        participation = (
            db.query(EventParticipation)
            .filter(
                and_(EventParticipation.event_id == event_id, EventParticipation.user_id == user_id)
            )
            .first()
        )

        if participation:
            db.delete(participation)
            db.commit()
            return True
        return False


event = CRUDEvent()
