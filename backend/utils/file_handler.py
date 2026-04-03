"""
utils/file_handler.py — Helpers for receiving and storing uploaded images

Keeping I/O logic here (separate from business logic) means the rest of
the pipeline never has to think about file paths, extensions, or disk writes.
"""

import uuid
import shutil
from pathlib import Path

from fastapi import UploadFile, HTTPException


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# All uploaded images land in this folder (created automatically if missing).
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Only these MIME types are accepted.  Extend this list as needed.
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

# Map MIME type → file extension so the saved file has the right suffix.
MIME_TO_EXT: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def validate_image(file: UploadFile) -> None:
    """
    Raise an HTTP 400 error if the uploaded file is not an accepted image type.

    FastAPI calls this before we touch the file contents, so bad uploads are
    rejected early and cheaply.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{file.content_type}'. "
                f"Accepted types: {', '.join(ALLOWED_MIME_TYPES)}."
            ),
        )


def save_upload(file: UploadFile) -> Path:
    """
    Persist the uploaded file to the UPLOAD_DIR with a unique filename.

    Using a UUID prevents collisions when many images are uploaded at once,
    and avoids leaking the original filename onto the server filesystem.

    Returns the Path where the file was saved.
    """
    ext = MIME_TO_EXT.get(file.content_type, ".bin")
    unique_name = f"{uuid.uuid4().hex}{ext}"
    destination = UPLOAD_DIR / unique_name

    # Write the file in streaming chunks to avoid loading it all into RAM.
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination


def cleanup_file(file_path: Path) -> None:
    """
    Delete a temporary file after the pipeline has finished with it.

    Wrapped in a try/except so a missing file never crashes the response.
    In production you might queue this for async cleanup instead.
    """
    try:
        file_path.unlink(missing_ok=True)
    except OSError:
        # Log and continue — a leftover temp file isn't worth a 500 error.
        pass


def get_file_metadata(file: UploadFile, saved_path: Path) -> dict:
    """
    Return a small dict of file-level facts to attach to the response metadata.
    """
    return {
        "original_filename": file.filename,
        "content_type": file.content_type,
        "saved_as": saved_path.name,
    }
