"""
services/yolo_service.py — Stage 1: UI Element Detection (dummy YOLO)

In a real system this would load a YOLOv8 model trained on UI screenshots
and run inference to find buttons, text blocks, icons, etc.

Right now it returns hard-coded realistic data so the rest of the pipeline
has something meaningful to work with.

REPLACING WITH A REAL MODEL LATER:
    1. Install ultralytics: `pip install ultralytics`
    2. Load your model: `model = YOLO("best.pt")`
    3. Run inference: `results = model(image_path)`
    4. Map results to the DetectedElement schema below.
"""

from pathlib import Path

from backend.models.response_model import DetectedElement, BoundingBox


# ---------------------------------------------------------------------------
# Dummy data — realistic bounding boxes for a typical app screenshot
# ---------------------------------------------------------------------------

_MOCK_ELEMENTS: list[dict] = [
    {"label": "button",    "confidence": 0.95, "x": 120, "y": 450, "w": 160, "h": 44},
    {"label": "button",    "confidence": 0.91, "x": 300, "y": 450, "w": 160, "h": 44},
    {"label": "text_block","confidence": 0.97, "x": 60,  "y": 80,  "w": 420, "h": 30},
    {"label": "text_block","confidence": 0.88, "x": 60,  "y": 130, "w": 360, "h": 20},
    {"label": "image",     "confidence": 0.93, "x": 60,  "y": 180, "w": 540, "h": 200},
    {"label": "input_field","confidence": 0.89,"x": 60,  "y": 400, "w": 380, "h": 40},
    {"label": "navbar",    "confidence": 0.99, "x": 0,   "y": 0,   "w": 660, "h": 60},
    {"label": "icon",      "confidence": 0.82, "x": 610, "y": 15,  "w": 30,  "h": 30},
]


# ---------------------------------------------------------------------------
# Public function
# ---------------------------------------------------------------------------

def detect_ui_elements(image_path: Path) -> list[DetectedElement]:
    """
    Run (dummy) YOLO detection on the screenshot at *image_path*.

    Parameters
    ----------
    image_path : Path
        Path to the saved screenshot on disk.

    Returns
    -------
    list[DetectedElement]
        Every UI element 'detected' in the image with its label,
        confidence score, and pixel bounding box.
    """
    # In a real implementation you would open the image here and pass it to
    # the model.  For now we just return the hard-coded list above.
    elements: list[DetectedElement] = []

    for item in _MOCK_ELEMENTS:
        element = DetectedElement(
            label=item["label"],
            confidence=item["confidence"],
            bounding_box=BoundingBox(
                x=item["x"],
                y=item["y"],
                width=item["w"],
                height=item["h"],
            ),
        )
        elements.append(element)

    return elements
