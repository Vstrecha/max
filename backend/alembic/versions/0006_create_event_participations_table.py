"""create_event_participations_table

Revision ID: 0006
Revises: 0005
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create event_participations table
    op.create_table(
        "event_participations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("event_id", sa.String(), nullable=False),
        sa.Column("participation_type", sa.CHAR(length=1), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_event_participations_id"), "event_participations", ["id"], unique=False
    )
    op.create_index(
        "ix_event_participations_user_id", "event_participations", ["user_id"], unique=False
    )
    op.create_index(
        "ix_event_participations_event_id", "event_participations", ["event_id"], unique=False
    )
    op.create_index(
        "ix_event_participations_type", "event_participations", ["participation_type"], unique=False
    )
    op.create_foreign_key(
        "fk_event_participations_user_id",
        "event_participations",
        "profiles",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_event_participations_event_id",
        "event_participations",
        "events",
        ["event_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_event_participations_event_id", "event_participations", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_event_participations_user_id", "event_participations", type_="foreignkey"
    )
    op.drop_index("ix_event_participations_type", table_name="event_participations")
    op.drop_index("ix_event_participations_event_id", table_name="event_participations")
    op.drop_index("ix_event_participations_user_id", table_name="event_participations")
    op.drop_index(op.f("ix_event_participations_id"), table_name="event_participations")
    op.drop_table("event_participations")
