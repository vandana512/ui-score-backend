"""
services/scoring_service.py — Stage 5: Final Score Computation

This service aggregates the outputs of every earlier stage into:
  1. A weighted overall score (0–100)
  2. A per-category score breakdown
  3. A ranked list of actionable suggestions

In a real system the weights would be tuned on labelled data.
For now they're sensible defaults that produce a realistic score.
"""

from backend.models.response_model import (
    LayoutAnalysis,
    SemanticAnalysis,
    ScoreBreakdown,
)


# ---------------------------------------------------------------------------
# Weights — must sum to 1.0
# ---------------------------------------------------------------------------

_WEIGHTS = {
    "layout":           0.30,
    "accessibility":    0.30,
    "visual_hierarchy": 0.20,
    "consistency":      0.20,
}


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------

def compute_score(
    layout: LayoutAnalysis,
    semantics: SemanticAnalysis,
) -> tuple[int, ScoreBreakdown, list[str]]:
    """
    Compute the overall UI quality score and actionable suggestions.

    Parameters
    ----------
    layout : LayoutAnalysis
        Structural metrics from the OpenCV stage.
    semantics : SemanticAnalysis
        UX / accessibility observations from the CLIP stage.

    Returns
    -------
    tuple of (overall_score, breakdown, suggestions)
        overall_score : int  — single 0–100 number
        breakdown     : ScoreBreakdown — per-category scores
        suggestions   : list[str]      — ordered improvement tips
    """

    # ------------------------------------------------------------------
    # 1. Derive per-category scores from the earlier pipeline stages.
    #    In a real system each of these would be calculated from real data.
    # ------------------------------------------------------------------

    layout_score = (
        layout.alignment_score * 0.4
        + layout.spacing_consistency * 0.3
        + layout.grid_adherence * 0.3
    )

    # Penalise 10 points for every accessibility flag (capped at 40 pts)
    accessibility_penalty = min(len(semantics.accessibility_flags) * 10, 40)
    accessibility_score = max(0.0, 100.0 - accessibility_penalty)

    # Visual hierarchy: driven by visual balance + a deduction for semantic issues
    semantic_penalty = min(len(semantics.detected_issues) * 8, 32)
    visual_hierarchy_score = max(0.0, layout.visual_balance - semantic_penalty)

    # Consistency: average of alignment and spacing scores
    consistency_score = (layout.alignment_score + layout.spacing_consistency) / 2

    breakdown = ScoreBreakdown(
        layout=round(layout_score, 1),
        accessibility=round(accessibility_score, 1),
        visual_hierarchy=round(visual_hierarchy_score, 1),
        consistency=round(consistency_score, 1),
    )

    # ------------------------------------------------------------------
    # 2. Compute the weighted overall score.
    # ------------------------------------------------------------------

    weighted = (
        breakdown.layout           * _WEIGHTS["layout"]
        + breakdown.accessibility  * _WEIGHTS["accessibility"]
        + breakdown.visual_hierarchy * _WEIGHTS["visual_hierarchy"]
        + breakdown.consistency    * _WEIGHTS["consistency"]
    )
    overall_score = int(round(weighted))

    # ------------------------------------------------------------------
    # 3. Generate suggestions ordered by impact (highest-penalty issues first).
    # ------------------------------------------------------------------

    suggestions = _build_suggestions(layout, semantics, breakdown)

    return overall_score, breakdown, suggestions


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _build_suggestions(
    layout: LayoutAnalysis,
    semantics: SemanticAnalysis,
    breakdown: ScoreBreakdown,
) -> list[str]:
    """
    Build an ordered list of concrete improvement recommendations.

    Rules:
    - Accessibility issues always come first (highest user impact).
    - Low-scoring layout areas come next.
    - Style observations come last (nice-to-have).
    """
    suggestions: list[str] = []

    # --- Accessibility (highest priority) ---
    if breakdown.accessibility < 80:
        suggestions.append(
            "Fix contrast ratios: aim for at least 4.5:1 for normal text (WCAG AA)."
        )
        suggestions.append(
            "Add visible focus indicators to all interactive elements for keyboard users."
        )
        suggestions.append(
            "Ensure all images have descriptive alt-text attributes."
        )

    # --- Layout ---
    if breakdown.layout < 75:
        suggestions.append(
            "Adopt a consistent 8 px or 4 px spacing grid across all elements."
        )
    if layout.alignment_score < 75:
        suggestions.append(
            "Align all interactive elements to the same 12-column grid to improve visual order."
        )
    if layout.spacing_consistency < 75:
        suggestions.append(
            "Standardise vertical rhythm: pick one spacing unit (e.g. 16 px) and use multiples."
        )

    # --- Visual hierarchy ---
    if breakdown.visual_hierarchy < 70:
        suggestions.append(
            "Reduce the number of competing focal points above the fold to one clear CTA."
        )
        suggestions.append(
            "Increase font-weight contrast between headings and body text to strengthen hierarchy."
        )

    # --- Consistency ---
    if breakdown.consistency < 75:
        suggestions.append(
            "Define a design token set (colours, spacing, type scale) and apply it consistently."
        )

    # --- Style observations (lowest priority) ---
    for obs in semantics.style_observations:
        suggestions.append(f"Style tip: {obs}")

    return suggestions
