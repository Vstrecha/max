"""
File Endpoints
FastAPI route handlers for file upload and management API.
"""

# --------------------------------------------------------------------------------

import uuid

from fastapi import APIRouter, Depends
from fastapi import File as FastAPIFile
from fastapi import HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.image_utils import convert_to_webp_and_resize, is_valid_image
from app.core.s3 import create_s3_client
from app.db.crud import files as crud_files
from app.db.crud import profiles as crud_profiles
from app.db.models import FileType
from app.schemas.files import File, FileUploadResponse

from ....api.v1.docs.examples.file_examples import (
    delete_file_examples,
    get_file_examples,
    get_my_files_examples,
    upload_file_examples,
)
from ....db.session import get_db

# --------------------------------------------------------------------------------

router = APIRouter()

# --------------------------------------------------------------------------------


def get_s3_client():
    """
    Get S3 client instance.

    Returns:
        S3Client: Configured S3 client.
    """
    return create_s3_client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        bucket=settings.S3_BUCKET,
        endpoint_url=settings.S3_ENDPOINT_URL,
        public_url=settings.S3_PUBLIC_URL,
        region=settings.S3_REGION,
    )


# --------------------------------------------------------------------------------


@router.post("/upload", response_model=FileUploadResponse, openapi_extra=upload_file_examples)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    file_type: FileType = FileType.AVATAR,
    request: Request = None,
    db: Session = Depends(get_db),
    s3_client=Depends(get_s3_client),
):
    """
    Upload an image file.

    Args:
        file (UploadFile): The file to upload.
        file_type (FileType): Type of file (avatar/event).
        request (Request): FastAPI request object.
        db (Session): Database session.
        s3_client (S3Client): S3 client instance.

    Returns:
        FileUploadResponse: File information and access token.
    """
    telegram_id = request.state.user_id

    # Read file content
    file_content = await file.read()

    # Validate file is an image (not GIF)
    if not is_valid_image(file_content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only images (not GIF) are allowed.",
        )

    # Convert to WebP and resize
    processed_image = convert_to_webp_and_resize(file_content)

    # Generate filename with .webp extension
    filename = f"{uuid.uuid4()}.webp"

    # Upload to S3
    try:
        url = s3_client.upload_file(
            file_bytes=processed_image, filename=filename, content_type="image/webp"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}",
        )

    # Save file record to database
    from app.schemas.files import FileCreate

    file_create = FileCreate(name=file.filename, type=file_type)
    db_file = crud_files.create_file(db, file_create, telegram_id, url)

    return FileUploadResponse(id=db_file.id, url=db_file.url)


# --------------------------------------------------------------------------------


@router.get("/", response_model=list[File], openapi_extra=get_my_files_examples)
async def get_my_files(
    file_type: FileType = None,
    skip: int = 0,
    limit: int = 100,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Get current user's files.

    Args:
        file_type (FileType, optional): Filter by file type.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        List[File]: List of user's files.
    """
    telegram_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, telegram_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if file_type:
        files = crud_files.get_user_files_by_type(db, telegram_id, file_type, skip, limit)
    else:
        files = crud_files.get_files_by_user(db, telegram_id, skip, limit)

    return files


# --------------------------------------------------------------------------------


@router.get("/{file_id}", response_model=File, openapi_extra=get_file_examples)
async def get_file(
    file_id: str,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Get a specific file by ID.

    Args:
        file_id (str): File ID.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        File: File information.
    """
    telegram_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, telegram_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    file = crud_files.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


# --------------------------------------------------------------------------------


@router.delete(
    "/{file_id}", status_code=status.HTTP_204_NO_CONTENT, openapi_extra=delete_file_examples
)
async def delete_file(
    file_id: str,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Delete a file by ID.

    Args:
        file_id (str): File ID.
        request (Request): FastAPI request object.
        db (Session): Database session.

    Returns:
        None: Always returns 204 (success).
    """
    user_id = request.state.user_id

    # Get user profile by telegram ID
    profile = crud_profiles.get_profile_by_telegram(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    file = crud_files.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # # Check if user owns this file
    # if file.user_id != profile.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own files"
    #     )

    crud_files.remove_file(db, file_id)
    return None
