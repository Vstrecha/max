"""convert_registration_dates_to_datetime

Revision ID: 0008
Revises: 0007
Create Date: 2025-11-10 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "events",
        "registration_start_date",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="registration_start_date::timestamp",
    )
    op.alter_column(
        "events",
        "registration_end_date",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="registration_end_date::timestamp",
    )


def downgrade() -> None:
    op.alter_column(
        "events",
        "registration_start_date",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using="registration_start_date::date",
    )
    op.alter_column(
        "events",
        "registration_end_date",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True,
        postgresql_using="registration_end_date::date",
    )
