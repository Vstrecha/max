"""
Database Session
Initialize SQLAlchemy engine and session for database access.
"""

# --------------------------------------------------------------------------------

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..core.config import settings

if os.getenv("TESTING", "false").lower() == "true":
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    connect_args = {"check_same_thread": False}
    poolclass = StaticPool
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    connect_args = {}
    poolclass = None

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    poolclass=poolclass,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------------------------------------------


def get_db():
    """
    Provide a database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
