"""
Base Model Class
Common base for all SQLAlchemy models with UUID generation.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr

# --------------------------------------------------------------------------------


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.

    Attributes:
        id (Any): Primary key of the model.
        __tablename__ (str): Table name inferred from class name.
    """

    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Automatically generate table name from class name.

        Returns:
            str: Lowercase class name as table name.
        """
        return cls.__name__.lower()

    @staticmethod
    def generate_id() -> str:
        """
        Generate a UUID4 string for model ID.

        Returns:
            str: UUID string.
        """
        return str(uuid.uuid4())
