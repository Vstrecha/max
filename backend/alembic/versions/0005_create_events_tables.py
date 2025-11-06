"""create events tables

Revision ID: 0005
Revises: 0004
Create Date: 2024-01-01 00:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create events table
    op.create_table(
        "events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("photo", sa.String(), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("place", sa.String(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=False),
        sa.Column("end_date", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("participants", sa.Integer(), nullable=True),
        sa.Column("creator", sa.String(), nullable=False),
        sa.Column("visability", sa.CHAR(length=1), nullable=False),
        sa.Column("repeatability", sa.CHAR(length=1), nullable=False),
        sa.Column("status", sa.CHAR(length=1), nullable=False),
        sa.Column("telegram_chat_link", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["creator"],
            ["profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["photo"],
            ["files.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)

    # Create event_participations table
    op.create_table(
        "event_participations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("event_id", sa.String(), nullable=False),
        sa.Column("participation_type", sa.CHAR(length=1), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["profiles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_event_participations_id"), "event_participations", ["id"], unique=False
    )

    # Add indexes for better performance
    op.create_index("ix_events_creator", "events", ["creator"])
    op.create_index("ix_events_start_date", "events", ["start_date"])
    op.create_index("ix_events_visability", "events", ["visability"])
    op.create_index("ix_events_status", "events", ["status"])
    op.create_index("ix_event_participations_user_id", "event_participations", ["user_id"])
    op.create_index("ix_event_participations_event_id", "event_participations", ["event_id"])
    op.create_index("ix_event_participations_type", "event_participations", ["participation_type"])


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_event_participations_type", table_name="event_participations")
    op.drop_index("ix_event_participations_event_id", table_name="event_participations")
    op.drop_index("ix_event_participations_user_id", table_name="event_participations")
    op.drop_index("ix_events_status", table_name="events")
    op.drop_index("ix_events_visability", table_name="events")
    op.drop_index("ix_events_start_date", table_name="events")
    op.drop_index("ix_events_creator", table_name="events")

    # Drop tables
    op.drop_index(op.f("ix_event_participations_id"), table_name="event_participations")
    op.drop_table("event_participations")
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_table("events")
