"""create_profiles_table

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create profiles table (depends on files for avatar)
    op.create_table(
        "profiles",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("gender", sa.String(1), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("avatar", sa.String(), nullable=True),
        sa.Column("university", sa.String(), nullable=True),
        sa.Column("bio", sa.String(), nullable=True),
        sa.Column("max_id", sa.BigInteger(), nullable=False),
        sa.Column("invited_by", sa.String(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_profiles_id"), "profiles", ["id"], unique=False)
    op.create_index("ix_profiles_max_id", "profiles", ["max_id"], unique=False)
    op.create_foreign_key(
        "fk_profiles_avatar", "profiles", "files", ["avatar"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        "fk_profiles_invited_by",
        "profiles",
        "profiles",
        ["invited_by"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_profiles_invited_by", "profiles", type_="foreignkey")
    op.drop_constraint("fk_profiles_avatar", "profiles", type_="foreignkey")
    op.drop_index("ix_profiles_max_id", table_name="profiles")
    op.drop_index(op.f("ix_profiles_id"), table_name="profiles")
    op.drop_table("profiles")
