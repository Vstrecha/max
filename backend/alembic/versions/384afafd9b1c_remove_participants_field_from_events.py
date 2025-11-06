"""remove_participants_field_from_events

Revision ID: 384afafd9b1c
Revises: 0008
Create Date: 2025-09-01 00:41:04.196081

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "384afafd9b1c"
down_revision: Union[str, Sequence[str], None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove participants field from events table."""
    # Drop the participants column from events table
    op.drop_column("events", "participants")


def downgrade() -> None:
    """Add back participants field to events table."""
    # Add back the participants column to events table
    op.add_column("events", sa.Column("participants", sa.Integer(), nullable=True))
