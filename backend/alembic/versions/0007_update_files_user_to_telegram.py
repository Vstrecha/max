"""update files.user_id to telegram_id bigint

Revision ID: 0007
Revises: 0006
Create Date: 2025-08-26 00:00:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Add new nullable column telegram_id
    op.add_column("files", sa.Column("telegram_id", sa.BigInteger(), nullable=True))

    # 2) Backfill telegram_id from profiles via user_id if user_id exists
    #    This assumes previous schema had files.user_id referencing profiles.id
    op.execute(
        """
        UPDATE files f
        SET telegram_id = p.telegram
        FROM profiles p
        WHERE f.telegram_id IS NULL AND f.user_id = p.id
        """
    )

    # 3) Make telegram_id NOT NULL
    op.alter_column("files", "telegram_id", existing_type=sa.BigInteger(), nullable=False)

    # 4) Create index on telegram_id
    op.create_index(op.f("ix_files_telegram_id"), "files", ["telegram_id"], unique=False)

    # 5) Drop foreign key and user_id column if exists
    # Depending on alembic naming, FK constraint name may vary; drop column directly if FK unnamed
    with op.batch_alter_table("files") as batch_op:
        # best-effort: drop user_id column
        try:
            batch_op.drop_column("user_id")
        except Exception:
            pass


def downgrade() -> None:
    # Recreate user_id as String and drop telegram_id; data loss possible on downgrade
    with op.batch_alter_table("files") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.String(), nullable=True))

    # Attempt to backfill user_id by joining profiles on telegram
    op.execute(
        """
        UPDATE files f
        SET user_id = p.id
        FROM profiles p
        WHERE f.telegram_id = p.telegram
        """
    )

    with op.batch_alter_table("files") as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.String(), nullable=False)

    op.drop_index(op.f("ix_files_telegram_id"), table_name="files")

    with op.batch_alter_table("files") as batch_op:
        batch_op.drop_column("telegram_id")
