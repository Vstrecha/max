"""
Create profiles table migration
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "profiles",
        sa.Column("id", sa.String(), primary_key=True, index=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("gender", sa.String(1), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("university", sa.String(), nullable=True),
        sa.Column("bio", sa.String(), nullable=True),
        sa.Column("telegram", sa.BigInteger(), nullable=True),
        sa.Column("invited_by", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["invited_by"], ["profiles.id"], ondelete="SET NULL"),
    )


def downgrade():
    op.drop_table("profiles")
