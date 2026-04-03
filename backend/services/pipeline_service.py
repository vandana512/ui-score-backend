"""
services/pipeline_service.py — Orchestrates the full analysis pipeline

This is the 'conductor' of the system.  It knows the order of stages and
passes outputs from one stage into the next, but it contains *no* analysis
logic itself — that lives in each individual service.

Pipeline stages (in order):
    1. yolo_service        → detect UI elements
    2. segmentation_service → identify layout regions
    3. opencv_service      → structural / alignment analysis
    4. clip_service        → semantic / UX analysis
    5. scoring_service     → aggregate a final score + suggestions

To add a new stage later, just import it here and call it in run_pipeline().
"""

import time
from pathlib import Path

from services.yolo_service import detect_ui_elements
from services.segmentation_service import segment_layout
from services.opencv_service import analyze_layout
from services.clip_service import analyze_semantics
from services.scoring_service import compute_score

from models.response_model import (
    AnalysisResponse,
    Issue,
)


# ---------------------------------------------------------------------------
# Issue assembly helper
# ---------------------------------------------------------------------------

def _collect_issues(layout_analysis, semantic_analysis) -> list[Issue]:
    """
    Combine problems found across the OpenCV and CLIP stages into a single
    ranked issue list that is easy for the frontend to display.

    Severity mapping:
      - alignment / spacing problems → 'medium'
      - accessibility flags          → 'high'
      - semantic / UX issues         → 'high'
      - style observations           → 'low'
    """
    issues: list[Issue] = []

    # Alignment issues (from OpenCV)
    for description in layout_analysis.alignment_issues:
        issues.append(Issue(type="alignment", description=description, severity="medium"))

    # Spacing issues (from OpenCV)
    for description in layout_analysis.spacing_issues:
        issues.append(Issue(type="spacing", description=description, severity="medium"))

    # Semantic / UX issues (from CLIP)
    for description in semantic_analysis.detected_issues:
        issues.append(Issue(type="ux", description=description, severity="high"))

    # Accessibility flags (from CLIP)
    for description in semantic_analysis.accessibility_flags:
        issues.append(Issue(type="accessibility", description=description, severity="high"))

    # Style observations (from CLIP)
    for description in semantic_analysis.style_observations:
        issues.append(Issue(type="style", description=description, severity="low"))

    return issues


# ---------------------------------------------------------------------------
# Main pipeline entry point
# ---------------------------------------------------------------------------

def run_pipeline(image_path: Path, file_metadata: dict) -> AnalysisResponse:
    """
    Execute every analysis stage in sequence and return the full report.

    Parameters
    ----------
    image_path : Path
        Path to the temporarily saved screenshot.
    file_metadata : dict
        Basic file info (name, type, size) to embed in the response.

    Returns
    -------
    AnalysisResponse
        The complete structured report ready to be serialised to JSON.
    """
    pipeline_start = time.perf_counter()

    # ------------------------------------------------------------------
    # Stage 1 — YOLO: detect individual UI elements
    # ------------------------------------------------------------------
    stage_start = time.perf_counter()
    elements = detect_ui_elements(image_path)
    yolo_ms = round((time.perf_counter() - stage_start) * 1000, 2)

    # ------------------------------------------------------------------
    # Stage 2 — Segmentation: identify broad layout regions
    # ------------------------------------------------------------------
    stage_start = time.perf_counter()
    regions = segment_layout(image_path)
    seg_ms = round((time.perf_counter() - stage_start) * 1000, 2)

    # ------------------------------------------------------------------
    # Stage 3 — OpenCV: structural / alignment analysis
    # ------------------------------------------------------------------
    stage_start = time.perf_counter()
    layout_analysis = analyze_layout(image_path)
    cv_ms = round((time.perf_counter() - stage_start) * 1000, 2)

    # ------------------------------------------------------------------
    # Stage 4 — CLIP: semantic / UX analysis
    # ------------------------------------------------------------------
    stage_start = time.perf_counter()
    semantic_analysis = analyze_semantics(image_path)
    clip_ms = round((time.perf_counter() - stage_start) * 1000, 2)

    # ------------------------------------------------------------------
    # Stage 5 — Scoring: aggregate all outputs into a single score
    # ------------------------------------------------------------------
    stage_start = time.perf_counter()
    overall_score, score_breakdown, suggestions = compute_score(
        layout=layout_analysis,
        semantics=semantic_analysis,
    )
    score_ms = round((time.perf_counter() - stage_start) * 1000, 2)

    # ------------------------------------------------------------------
    # Assemble the issue list from all stages
    # ------------------------------------------------------------------
    issues = _collect_issues(layout_analysis, semantic_analysis)

    # ------------------------------------------------------------------
    # Build timing metadata (useful for debugging and optimisation later)
    # ------------------------------------------------------------------
    total_ms = round((time.perf_counter() - pipeline_start) * 1000, 2)

    metadata = {
        **file_metadata,
        "pipeline_timing_ms": {
            "yolo":        yolo_ms,
            "segmentation": seg_ms,
            "opencv":      cv_ms,
            "clip":        clip_ms,
            "scoring":     score_ms,
            "total":       total_ms,
        },
        "elements_count": len(elements),
        "regions_count":  len(regions),
        "issues_count":   len(issues),
    }

    # ------------------------------------------------------------------
    # Return the fully assembled response
    # ------------------------------------------------------------------
    return AnalysisResponse(
        score=overall_score,
        score_breakdown=score_breakdown,
        issues=issues,
        elements_detected=elements,
        segmented_regions=regions,
        layout_analysis=layout_analysis,
        semantic_analysis=semantic_analysis,
        suggestions=suggestions,
        metadata=metadata,
    )
