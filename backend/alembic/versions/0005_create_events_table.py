"""create_events_table

Revision ID: 0005
Revises: 0004
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=True),
        sa.Column("registration_start_date", sa.Date(), nullable=True),
        sa.Column("registration_end_date", sa.Date(), nullable=True),
        sa.Column("creator", sa.String(), nullable=False),
        sa.Column("status", sa.CHAR(length=1), nullable=False, server_default="A"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)
    op.create_index("ix_events_creator", "events", ["creator"], unique=False)
    op.create_index("ix_events_start_date", "events", ["start_date"], unique=False)
    op.create_index("ix_events_status", "events", ["status"], unique=False)
    op.create_foreign_key(
        "fk_events_creator", "events", "profiles", ["creator"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_events_photo", "events", "files", ["photo"], ["id"], ondelete="SET NULL"
    )


def downgrade() -> None:
    op.drop_constraint("fk_events_photo", "events", type_="foreignkey")
    op.drop_constraint("fk_events_creator", "events", type_="foreignkey")
    op.drop_index("ix_events_status", table_name="events")
    op.drop_index("ix_events_start_date", table_name="events")
    op.drop_index("ix_events_creator", table_name="events")
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_table("events")
