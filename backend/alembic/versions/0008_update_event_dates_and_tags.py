"""Update event dates and tags

Revision ID: 0008
Revises: 0007
Create Date: 2024-01-01 00:00:00.000000

"""

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change start_date and end_date from DATETIME to DATE
    # SQLite doesn't support direct column type changes, so we need to recreate
    # For now, we'll keep the existing columns and handle the conversion in the
    # application layer
    # In a production PostgreSQL environment, you would use:
    # op.alter_column('events', 'start_date', type_=sa.Date())
    # op.alter_column('events', 'end_date', type_=sa.Date())
    pass


def downgrade() -> None:
    # Revert back to DATETIME if needed
    # op.alter_column('events', 'start_date', type_=sa.DateTime())
    # op.alter_column('events', 'end_date', type_=sa.DateTime())
    pass
