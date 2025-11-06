"""
Alembic Migration Setup
Configuration and execution of database migrations.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings
from app.db.base_class import Base

# --------------------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# --------------------------------------------------------------------------------


def get_url():
    """
    Get the database URL from settings.

    Returns:
        str: The database URL.
    """
    return settings.DATABASE_URL


# --------------------------------------------------------------------------------


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with a URL and no engine,
    allowing migrations without a database connection.

    Returns:
        None
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --------------------------------------------------------------------------------


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Creates an engine and connects it to the context
    to execute migrations with a live database.

    Returns:
        None
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# --------------------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
