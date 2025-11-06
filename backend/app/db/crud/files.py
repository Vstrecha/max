"""
File CRUD
CRUD operations for File model in the database.
"""

# --------------------------------------------------------------------------------

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import File, FileType
from app.schemas.files import FileCreate

# --------------------------------------------------------------------------------


def create_file(db: Session, obj_in: FileCreate, max_id: int, url: str) -> File:
    """
    Create a new file in the database.

    Args:
        db (Session): Database session.
        obj_in (FileCreate): Data for creating a file.
        max_id (int): Max ID of the user who uploaded the file.
        url (str): Public URL to the file in S3.

    Returns:
        File: Created file instance.
    """
    db_obj = File(
        id=str(uuid.uuid4()),
        name=obj_in.name,
        url=url,
        max_id=max_id,
        type=obj_in.type,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# --------------------------------------------------------------------------------


def get_file(db: Session, file_id: str) -> Optional[File]:
    """
    Get a file by ID.

    Args:
        db (Session): Database session.
        file_id (str): File ID.

    Returns:
        Optional[File]: File instance or None if not found.
    """
    return db.query(File).filter(File.id == file_id).first()


# --------------------------------------------------------------------------------


def get_files_by_user(
    db: Session,
    max_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[File]:
    """
    Get a list of files uploaded by a specific user.

    Args:
        db (Session): Database session.
        max_id (int): Max ID.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[File]: List of file objects.
    """
    return db.query(File).filter(File.max_id == max_id).offset(skip).limit(limit).all()


# --------------------------------------------------------------------------------


def get_files_by_type(
    db: Session,
    file_type: FileType,
    skip: int = 0,
    limit: int = 100,
) -> list[File]:
    """
    Get a list of files by type.

    Args:
        db (Session): Database session.
        file_type (FileType): Type of files to retrieve.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[File]: List of file objects.
    """
    return db.query(File).filter(File.type == file_type).offset(skip).limit(limit).all()


# --------------------------------------------------------------------------------


def get_user_files_by_type(
    db: Session,
    max_id: int,
    file_type: FileType,
    skip: int = 0,
    limit: int = 100,
) -> list[File]:
    """
    Get a list of files uploaded by a specific user with specific type.

    Args:
        db (Session): Database session.
        max_id (int): Max ID.
        file_type (FileType): Type of files to retrieve.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[File]: List of file objects.
    """
    return (
        db.query(File)
        .filter(File.max_id == max_id, File.type == file_type)
        .offset(skip)
        .limit(limit)
        .all()
    )


# --------------------------------------------------------------------------------


def remove_file(db: Session, file_id: str) -> Optional[File]:
    """
    Remove a file from the database by ID.

    Args:
        db (Session): Database session.
        file_id (str): File ID.

    Returns:
        Optional[File]: Removed file instance or None if not found.
    """
    obj = db.query(File).filter(File.id == file_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# --------------------------------------------------------------------------------


def delete_all_files(db: Session) -> None:
    """
    Delete all files from the database.
    Used for testing purposes.

    Args:
        db (Session): Database session.
    """
    db.query(File).delete()
    db.commit()
