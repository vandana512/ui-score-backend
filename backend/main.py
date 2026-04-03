"""
main.py — Entry point for the UI Analysis Pipeline API

This file creates the FastAPI app and registers all routes.
Think of it as the 'front door' of the backend system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.analyze import router as analyze_router

# ---------------------------------------------------------------------------
# App Setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="UI Analysis Pipeline API",
    description=(
        "A modular backend that accepts a screenshot and runs a dummy "
        "CV pipeline (YOLO → Segmentation → OpenCV → CLIP → Scoring) "
        "to return a structured UI quality report."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — allows a frontend (or Postman) to call this API from any origin.
# In production you'd restrict 'allow_origins' to your actual domain.
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register route modules
# ---------------------------------------------------------------------------

app.include_router(analyze_router, prefix="/api", tags=["Analysis"])


# ---------------------------------------------------------------------------
# Health-check endpoint — useful to confirm the server is running
# ---------------------------------------------------------------------------

@app.get("/health", summary="Health Check")
def health_check() -> dict:
    """Returns a simple OK status so you can verify the server is alive."""
    return {"status": "ok", "message": "UI Analysis API is running."}
