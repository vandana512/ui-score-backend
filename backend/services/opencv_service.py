"""
services/opencv_service.py — Stage 3: Structural Layout Analysis (dummy OpenCV)

In a real system this would use OpenCV (cv2) to:
  - Detect element edges and measure alignment to a grid
  - Calculate spacing between elements
  - Measure visual balance (mass distribution across the viewport)
  - Flag elements that break the grid

REPLACING WITH REAL OPENCV LATER:
    1. `pip install opencv-python`
    2. Load image: `img = cv2.imread(str(image_path))`
    3. Use contour detection, Hough lines, or custom grid logic.
    4. Fill the LayoutAnalysis fields with measured values.
"""

from pathlib import Path

from models.response_model import LayoutAnalysis


# ---------------------------------------------------------------------------
# Dummy data
# ---------------------------------------------------------------------------

_MOCK_ALIGNMENT_ISSUES = [
    "CTA button is 8 px left of the expected 12-column grid boundary.",
    "Footer text does not align with the left margin of the content area.",
]

_MOCK_SPACING_ISSUES = [
    "Inconsistent vertical spacing between hero image and body text (32 px vs 16 px elsewhere).",
    "Input field and submit button have unequal horizontal padding.",
]


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------

def analyze_layout(image_path: Path) -> LayoutAnalysis:
    """
    Run (dummy) OpenCV structural analysis on the screenshot.

    Parameters
    ----------
    image_path : Path
        Path to the saved screenshot on disk.

    Returns
    -------
    LayoutAnalysis
        Numeric scores (0–100) for key structural properties plus plain-
        text lists of specific alignment and spacing problems found.
    """
    return LayoutAnalysis(
        # Scores are out of 100.  Lower = worse.
        alignment_score=74.0,
        spacing_consistency=68.5,
        visual_balance=81.0,
        grid_adherence=70.0,

        # Human-readable descriptions of each problem detected.
        alignment_issues=_MOCK_ALIGNMENT_ISSUES,
        spacing_issues=_MOCK_SPACING_ISSUES,
    )
