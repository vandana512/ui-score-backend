from backend.core.clip_scoring import get_clip_score

def run_clip_module(image_path: str, category: str):

    score = get_clip_score(image_path, category)

    return {
        "clip_score": float(score)
    }


# """
# services/clip_service.py — Stage 4: Semantic & UX Analysis (dummy CLIP)

# In a real system this would use OpenAI's CLIP model to embed the screenshot
# and compare it against text prompts such as:
#   - "a UI with low contrast text"
#   - "a cluttered, crowded layout"
#   - "a clean, accessible design"

# The cosine similarity scores would tell us which UX issues are present.

# REPLACING WITH REAL CLIP LATER:
#     1. `pip install transformers torch`
#     2. Load model: `model, preprocess = clip.load("ViT-B/32")`
#     3. Encode the image and a bank of issue prompts.
#     4. Rank prompts by similarity score → detected_issues.
# """

# from pathlib import Path

# from models.response_model import SemanticAnalysis


# # ---------------------------------------------------------------------------
# # Dummy data
# # ---------------------------------------------------------------------------

# _MOCK_DETECTED_ISSUES = [
#     "Low contrast between body text and background (estimated contrast ratio: 2.8:1, WCAG AA requires 4.5:1).",
#     "Crowded layout — multiple focal points compete for user attention above the fold.",
#     "CTA button colour is too similar to the surrounding background.",
# ]

# _MOCK_ACCESSIBILITY_FLAGS = [
#     "No visible focus indicators on interactive elements.",
#     "Images likely lack alt-text (inferred from layout density).",
#     "Font size in footer region appears below 12 px minimum.",
# ]

# _MOCK_STYLE_OBSERVATIONS = [
#     "Colour palette is cohesive but low-energy — consider a stronger accent colour.",
#     "Typography hierarchy is shallow; only two visual weight levels detected.",
#     "Hero image dominates ~30 % of viewport — ensure it supports rather than distracts from the CTA.",
# ]


# # ---------------------------------------------------------------------------
# # Public function
# # ---------------------------------------------------------------------------

# def analyze_semantics(image_path: Path) -> SemanticAnalysis:
#     """
#     Run (dummy) CLIP semantic analysis on the screenshot.

#     Parameters
#     ----------
#     image_path : Path
#         Path to the saved screenshot on disk.

#     Returns
#     -------
#     SemanticAnalysis
#         Three lists:
#           - detected_issues    : concrete UX/design problems
#           - accessibility_flags: WCAG / accessibility concerns
#           - style_observations : aesthetic observations (not blocking, but notable)
#     """
#     return SemanticAnalysis(
#         detected_issues=_MOCK_DETECTED_ISSUES,
#         accessibility_flags=_MOCK_ACCESSIBILITY_FLAGS,
#         style_observations=_MOCK_STYLE_OBSERVATIONS,
#     )
