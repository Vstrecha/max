"""create_qr_scans_table

Revision ID: 0007
Revises: 0006
Create Date: 2025-01-01 00:00:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create qr_scans table
    op.create_table(
        "qr_scans",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("participation_id", sa.String(), nullable=False),
        sa.Column("scanned_by_user_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "scanned_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_qr_scans_id"), "qr_scans", ["id"], unique=False)
    op.create_index("ix_qr_scans_participation_id", "qr_scans", ["participation_id"], unique=False)
    op.create_index(
        "ix_qr_scans_scanned_by_user_id", "qr_scans", ["scanned_by_user_id"], unique=False
    )
    op.create_foreign_key(
        "fk_qr_scans_participation_id",
        "qr_scans",
        "event_participations",
        ["participation_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_qr_scans_participation_id", "qr_scans", type_="foreignkey")
    op.drop_index("ix_qr_scans_scanned_by_user_id", table_name="qr_scans")
    op.drop_index("ix_qr_scans_participation_id", table_name="qr_scans")
    op.drop_index(op.f("ix_qr_scans_id"), table_name="qr_scans")
    op.drop_table("qr_scans")
