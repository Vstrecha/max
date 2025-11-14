"""create_files_table

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create files table (no dependencies)
    op.create_table(
        "files",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("max_id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_id"), "files", ["id"], unique=False)
    op.create_index("ix_files_max_id", "files", ["max_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_files_max_id", table_name="files")
    op.drop_index(op.f("ix_files_id"), table_name="files")
    op.drop_table("files")
