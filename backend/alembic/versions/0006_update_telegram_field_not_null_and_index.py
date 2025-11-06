"""update telegram field not null and add indexes

Revision ID: 0006
Revises: 0005
Create Date: 2024-01-22 12:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create index on telegram field if it doesn't exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)

    # Check if telegram index exists
    existing_indexes = [idx["name"] for idx in inspector.get_indexes("profiles")]
    if "ix_profiles_telegram" not in existing_indexes:
        op.create_index(op.f("ix_profiles_telegram"), "profiles", ["telegram"], unique=False)

    # Make telegram field not nullable
    # First, ensure there are no NULL values in telegram field
    op.execute("UPDATE profiles SET telegram = 0 WHERE telegram IS NULL")

    # Then alter the column to be not nullable
    op.alter_column("profiles", "telegram", existing_type=sa.BigInteger(), nullable=False)

    # Create indexes on user_id fields in friends table if they don't exist
    existing_indexes = [idx["name"] for idx in inspector.get_indexes("friends")]
    if "ix_friends_user_1" not in existing_indexes:
        op.create_index(op.f("ix_friends_user_1"), "friends", ["user_1"], unique=False)

    if "ix_friends_user_2" not in existing_indexes:
        op.create_index(op.f("ix_friends_user_2"), "friends", ["user_2"], unique=False)

    existing_indexes = [idx["name"] for idx in inspector.get_indexes("event_participations")]
    if "ix_event_participations_user_id" not in existing_indexes:
        op.create_index(
            op.f("ix_event_participations_user_id"),
            "event_participations",
            ["user_id"],
            unique=False,
        )

    if "ix_event_participations_event_id" not in existing_indexes:
        op.create_index(
            op.f("ix_event_participations_event_id"),
            "event_participations",
            ["event_id"],
            unique=False,
        )


def downgrade() -> None:
    # Remove the index
    op.drop_index(op.f("ix_profiles_telegram"), table_name="profiles")

    # Make telegram field nullable again
    op.alter_column("profiles", "telegram", existing_type=sa.BigInteger(), nullable=True)

    # Remove indexes on user_id fields in friends table
    op.drop_index(op.f("ix_friends_user_1"), table_name="friends")
    op.drop_index(op.f("ix_friends_user_2"), table_name="friends")

    # Remove indexes on user_id and event_id fields in event_participations table
    op.drop_index(op.f("ix_event_participations_user_id"), table_name="event_participations")
    op.drop_index(op.f("ix_event_participations_event_id"), table_name="event_participations")
