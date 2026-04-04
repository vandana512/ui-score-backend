"""
routes/analyze.py — Route definition for POST /analyze-ui

This file is only responsible for:
  1. Accepting the HTTP request
  2. Validating & saving the uploaded file
  3. Delegating to the pipeline service
  4. Returning the JSON response (or a helpful error)

All business logic lives in the service layer — never in the route.
"""

from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.utils.file_handler import validate_image, save_upload, cleanup_file, get_file_metadata
from backend.services.pipeline_service import run_pipeline
from backend.models.response_model import AnalysisResponse


# ---------------------------------------------------------------------------
# Router — will be registered in main.py under the /api prefix
# ---------------------------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /api/analyze-ui
# ---------------------------------------------------------------------------

@router.post(
    "/analyze-ui",
    response_model=AnalysisResponse,
    summary="Analyse a UI screenshot",
    description=(
        "Upload a screenshot (JPEG / PNG / WebP / GIF) and receive a structured "
        "report that includes detected UI elements, layout analysis, UX issues, "
        "accessibility flags, and an overall quality score."
    ),
)
async def analyze_ui(
    image: UploadFile = File(...),
    category: str = "dashboard"   # 👈 ADD THIS
) -> AnalysisResponse:
    """
    Full pipeline handler.

    Steps
    -----
    1. Check that a file was actually uploaded.
    2. Validate the MIME type.
    3. Save the file temporarily.
    4. Run the analysis pipeline.
    5. Delete the temp file.
    6. Return the report.
    """

    # ------------------------------------------------------------------
    # Step 1 — Ensure a file was sent
    # ------------------------------------------------------------------
    if not image or not image.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded. Please attach a screenshot via multipart/form-data.",
        )

    # ------------------------------------------------------------------
    # Step 2 — Validate MIME type (rejects PDFs, zips, etc.)
    # ------------------------------------------------------------------
    validate_image(image)

    # ------------------------------------------------------------------
    # Step 3 — Persist the file so the pipeline can read it from disk
    # ------------------------------------------------------------------
    saved_path: Path = save_upload(image)
    file_meta = get_file_metadata(image, saved_path)

    # ------------------------------------------------------------------
    # Step 4 — Run the pipeline (YOLO → Seg → CV → CLIP → Score)
    #          Wrapped in try/finally so temp files are always cleaned up.
    # ------------------------------------------------------------------
    try:
        report: AnalysisResponse = run_pipeline(
            image_path=saved_path,
            file_metadata=file_meta,
            category=category   # 👈 ADD THIS
        )
    except Exception as exc:
        # Surface unexpected errors as a 500 with a readable message.
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(exc)}",
        ) from exc
    finally:
        # ------------------------------------------------------------------
        # Step 5 — Clean up the temporary file regardless of success/failure
        # ------------------------------------------------------------------
        cleanup_file(saved_path)

    # ------------------------------------------------------------------
    # Step 6 — Return the structured JSON report
    # ------------------------------------------------------------------
    return report
