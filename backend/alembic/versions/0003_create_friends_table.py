"""create_friends_table

Revision ID: 0003
Revises: 0002
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create friends table
    op.create_table(
        "friends",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_1", sa.String(), nullable=False),
        sa.Column("user_2", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_1", "user_2", name="uq_friends_users"),
    )
    op.create_index(op.f("ix_friends_id"), "friends", ["id"], unique=False)
    op.create_index("ix_friends_user_1", "friends", ["user_1"], unique=False)
    op.create_index("ix_friends_user_2", "friends", ["user_2"], unique=False)
    op.create_foreign_key(
        "fk_friends_user_1", "friends", "profiles", ["user_1"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_friends_user_2", "friends", "profiles", ["user_2"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("fk_friends_user_2", "friends", type_="foreignkey")
    op.drop_constraint("fk_friends_user_1", "friends", type_="foreignkey")
    op.drop_index("ix_friends_user_2", table_name="friends")
    op.drop_index("ix_friends_user_1", table_name="friends")
    op.drop_index(op.f("ix_friends_id"), table_name="friends")
    op.drop_table("friends")
