# UI Analysis Pipeline — Backend

A modular FastAPI backend that accepts a UI screenshot and returns a structured
quality report by running a simulated CV pipeline.

```
YOLO → Segmentation → OpenCV → CLIP → Scoring
```

All pipeline stages are **dummy/mock** — no real ML models are loaded.
Each service is designed so you can drop in a real model later with minimal changes.

---

## Quick Start

### 1. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn main:app --reload
```

Server runs at **http://localhost:8000**

### 3. Open the interactive docs

Visit **http://localhost:8000/docs** for the Swagger UI — you can upload an
image and see the full JSON response directly in the browser.

---

## Project Structure

```
backend/
├── main.py                      ← App setup, CORS, router registration
│
├── routes/
│   └── analyze.py               ← POST /api/analyze-ui endpoint
│
├── services/
│   ├── pipeline_service.py      ← Orchestrates all stages in order
│   ├── yolo_service.py          ← Stage 1: UI element detection
│   ├── segmentation_service.py  ← Stage 2: Layout region segmentation
│   ├── opencv_service.py        ← Stage 3: Structural layout analysis
│   ├── clip_service.py          ← Stage 4: Semantic / UX analysis
│   └── scoring_service.py       ← Stage 5: Score computation
│
├── utils/
│   └── file_handler.py          ← File I/O, validation, cleanup
│
├── models/
│   └── response_model.py        ← Pydantic response schema
│
├── uploads/                     ← Temp storage (auto-created, auto-cleaned)
└── requirements.txt
```

---

## API

### `POST /api/analyze-ui`

| Field  | Type            | Description              |
|--------|-----------------|--------------------------|
| image  | file (required) | JPEG / PNG / WebP / GIF  |

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/analyze-ui \
  -F "image=@screenshot.png"
```

**Response shape:**
```json
{
  "score": 72,
  "score_breakdown": { "layout": 71.1, "accessibility": 70.0, ... },
  "issues": [
    { "type": "accessibility", "description": "...", "severity": "high" }
  ],
  "elements_detected": [ { "label": "button", "confidence": 0.95, ... } ],
  "segmented_regions": [ { "region": "navbar", "coverage_percent": 9.1 } ],
  "layout_analysis": { "alignment_score": 74.0, ... },
  "semantic_analysis": { "detected_issues": [...], ... },
  "suggestions": ["Fix contrast ratios: aim for at least 4.5:1 ...", ...],
  "metadata": { "pipeline_timing_ms": { "total": 1.23 }, ... }
}
```

---

## Replacing a Dummy Stage with a Real Model

Each service file has a **"REPLACING WITH A REAL MODEL LATER"** section
explaining exactly what to change.  The function signature stays the same,
so the rest of the pipeline requires zero edits.

---

## Health Check

```bash
curl http://localhost:8000/health
# → {"status": "ok", "message": "UI Analysis API is running."}
```
