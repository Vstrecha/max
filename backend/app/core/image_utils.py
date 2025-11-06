"""
Image processing utilities
Handles image conversion, resizing, and validation.
"""

# --------------------------------------------------------------------------------

import io

from PIL import Image, ImageOps, UnidentifiedImageError

# --------------------------------------------------------------------------------


def is_valid_image(file_bytes: bytes) -> bool:
    """
    Check if the file is a valid image (not GIF).

    Args:
        file_bytes (bytes): File content in bytes.

    Returns:
        bool: True if valid image, False otherwise.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Check if it's a GIF (animated or static)
        if image.format == "GIF":
            return False
        return True
    except (UnidentifiedImageError, Exception):
        return False


# --------------------------------------------------------------------------------


def convert_to_webp_and_resize(file_bytes: bytes, max_size: int = 1024) -> bytes:
    """
    Convert image to WebP format and resize to max_size on longest side.

    Args:
        file_bytes (bytes): Original image bytes.
        max_size (int): Maximum size for the longest side.

    Returns:
        bytes: Processed image in WebP format.
    """
    # Open image
    image = Image.open(io.BytesIO(file_bytes))

    # Fix orientation using EXIF if present
    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    # Convert to RGB if necessary (WebP doesn't support RGBA)
    if image.mode in ("RGBA", "LA", "P"):
        # Create white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "P":
            image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = background
    elif image.mode != "RGB":
        image = image.convert("RGB")

    # Resize image
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int(height * max_size / width)
    else:
        new_height = max_size
        new_width = int(width * max_size / height)

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Convert to WebP
    output = io.BytesIO()
    image.save(output, format="WEBP", quality=85, optimize=True)
    return output.getvalue()


# --------------------------------------------------------------------------------


def get_image_info(file_bytes: bytes) -> tuple[int, int, str]:
    """
    Get image dimensions and format.

    Args:
        file_bytes (bytes): Image file bytes.

    Returns:
        Tuple[int, int, str]: Width, height, and format.
    """
    image = Image.open(io.BytesIO(file_bytes))
    return image.size[0], image.size[1], image.format or "Unknown"
