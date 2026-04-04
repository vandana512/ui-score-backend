"""
models/response_model.py — Data shapes for the API response

Pydantic models act like typed contracts: they define exactly what the
JSON response will look like and validate it automatically.

When you later swap dummy data for real ML output, these models ensure
the response shape never accidentally changes.
"""

from typing import Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Sub-models (building blocks of the final response)
# ---------------------------------------------------------------------------

class Issue(BaseModel):
    """Represents a single UX / design problem found in the screenshot."""

    type: str = Field(..., description="Category of the issue, e.g. 'alignment', 'contrast'.")
    description: str = Field(..., description="Human-readable explanation of the problem.")
    severity: str = Field(..., description="One of: 'low', 'medium', 'high'.")


class BoundingBox(BaseModel):
    """Pixel coordinates of a detected UI element."""

    x: int = Field(..., description="Left edge (pixels from left of image).")
    y: int = Field(..., description="Top edge (pixels from top of image).")
    width: int = Field(..., description="Width of the bounding box in pixels.")
    height: int = Field(..., description="Height of the bounding box in pixels.")


class DetectedElement(BaseModel):
    """A UI element spotted by the YOLO stage."""

    label: str = Field(..., description="Element type, e.g. 'button', 'text', 'image'.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence (0–1).")
    bounding_box: BoundingBox


class SegmentedRegion(BaseModel):
    """A broad layout region returned by the Segmentation stage."""

    region: str = Field(..., description="Region name, e.g. 'header', 'footer', 'sidebar'.")
    coverage_percent: float = Field(
        ..., ge=0.0, le=100.0,
        description="What percentage of the total image this region occupies."
    )


class LayoutAnalysis(BaseModel):
    """Structural metrics produced by the OpenCV stage."""

    alignment_score: float = Field(..., ge=0.0, le=100.0)
    spacing_consistency: float = Field(..., ge=0.0, le=100.0)
    visual_balance: float = Field(..., ge=0.0, le=100.0)
    grid_adherence: float = Field(..., ge=0.0, le=100.0)
    alignment_issues: list[str]
    spacing_issues: list[str]


class SemanticAnalysis(BaseModel):
    """UX / semantic observations produced by the CLIP stage."""

    detected_issues: list[str]
    accessibility_flags: list[str]
    style_observations: list[str]


class ScoreBreakdown(BaseModel):
    """Per-category scores that feed into the overall score."""

    layout: float = Field(..., ge=0.0, le=100.0)
    accessibility: float = Field(..., ge=0.0, le=100.0)
    visual_hierarchy: float = Field(..., ge=0.0, le=100.0)
    consistency: float = Field(..., ge=0.0, le=100.0)


# ---------------------------------------------------------------------------
# Top-level response
# ---------------------------------------------------------------------------

class AnalysisResponse(BaseModel):
    """
    The complete response returned by POST /api/analyze-ui.

    Every field below maps to one stage of the pipeline.
    """

    score: int = Field(..., ge=0, le=100, description="Overall UI quality score (0-100).")
    clip_score: float = Field(..., ge=0.0, le=1.0, description="CLIP similarity score (0-1)")  # 👈 ADD THIS
    score_breakdown: ScoreBreakdown
    issues: list[Issue] = Field(..., description="All UX/design problems found.")
    elements_detected: list[DetectedElement] = Field(
        ..., description="UI elements found by the YOLO stage."
    )
    segmented_regions: list[SegmentedRegion] = Field(
        ..., description="Layout regions from the Segmentation stage."
    )
    layout_analysis: LayoutAnalysis = Field(
        ..., description="Structural metrics from the OpenCV stage."
    )
    semantic_analysis: SemanticAnalysis = Field(
        ..., description="UX observations from the CLIP stage."
    )
    suggestions: list[str] = Field(..., description="Actionable improvement recommendations.")
    metadata: dict[str, Any] = Field(..., description="Pipeline run metadata (timing, file info, etc.).")
