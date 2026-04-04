"""
services/segmentation_service.py — Stage 2: Layout Region Segmentation (dummy)

In a real system this would use a semantic segmentation model (e.g. a
fine-tuned SegFormer or SAM) to split the screenshot into named regions
like header, sidebar, content, footer.

REPLACING WITH A REAL MODEL LATER:
    1. Load your segmentation model.
    2. Run a forward pass on the image tensor.
    3. Map each predicted class to a region name + coverage %.
    4. Return the list below using the same SegmentedRegion schema.
"""

from pathlib import Path

from backend.models.response_model import SegmentedRegion


# ---------------------------------------------------------------------------
# Dummy data — realistic region breakdown for a standard web page screenshot
# ---------------------------------------------------------------------------

_MOCK_REGIONS: list[dict] = [
    {"region": "navbar",        "coverage_percent": 9.1},
    {"region": "hero_image",    "coverage_percent": 30.3},
    {"region": "content_area",  "coverage_percent": 40.5},
    {"region": "sidebar",       "coverage_percent": 12.1},
    {"region": "footer",        "coverage_percent": 8.0},
]


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------

def segment_layout(image_path: Path) -> list[SegmentedRegion]:
    """
    Run (dummy) segmentation on the screenshot at *image_path*.

    Parameters
    ----------
    image_path : Path
        Path to the saved screenshot on disk.

    Returns
    -------
    list[SegmentedRegion]
        Named layout regions, each annotated with the percentage of the
        total image area it occupies.  Percentages should sum to ~100 %.
    """
    regions: list[SegmentedRegion] = [
        SegmentedRegion(
            region=item["region"],
            coverage_percent=item["coverage_percent"],
        )
        for item in _MOCK_REGIONS
    ]
    return regions
