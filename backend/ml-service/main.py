from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(title="GraamSehat ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load symptom columns ──────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SYMPTOM_COLS_PATH = os.path.join(DATA_DIR, "symptom_cols.json")
SYMPTOM_MAP_PATH  = os.path.join(DATA_DIR, "symptom_map.json")

try:
    with open(SYMPTOM_COLS_PATH) as f:
        SYMPTOM_COLS = json.load(f)
except FileNotFoundError:
    SYMPTOM_COLS = []

try:
    with open(SYMPTOM_MAP_PATH) as f:
        SYMPTOM_MAP = json.load(f)   # hindi_word -> english_symptom
except FileNotFoundError:
    SYMPTOM_MAP = {}

# ── Hard RED signs (always override) ─────────────────────────────────
HARD_RED_SIGNS = [
    "stiff_neck", "coma", "chest_pain", "altered_sensorium",
    "stomach_bleeding", "blood_in_sputum", "weakness_of_one_body_side",
    "slurred_speech", "loss_of_balance", "unsteadiness",
]

# ── Symptom risk weights ──────────────────────────────────────────────
RED_SYMPTOMS = {
    "chest_pain": 3, "breathlessness": 3, "coma": 3,
    "altered_sensorium": 3, "stiff_neck": 3, "blood_in_sputum": 3,
    "stomach_bleeding": 3, "bloody_stool": 2, "fast_heart_rate": 2,
    "slurred_speech": 3, "loss_of_balance": 2, "weakness_of_one_body_side": 3,
    "pain_behind_the_eyes": 2, "red_spots_over_body": 2,
}
YELLOW_SYMPTOMS = {
    "high_fever": 2, "vomiting": 1, "diarrhoea": 1, "headache": 1,
    "joint_pain": 1, "muscle_pain": 1, "fatigue": 1, "nausea": 1,
    "dehydration": 2, "swelled_lymph_nodes": 2, "skin_rash": 1,
    "abdominal_pain": 1, "back_pain": 1, "mild_fever": 1,
    "swelling_joints": 2, "palpitations": 2, "shivering": 1,
    "chills": 1, "sweating": 1, "loss_of_appetite": 1,
}


class PredictRequest(BaseModel):
    symptoms: Optional[List[int]] = None   # one-hot vector (length = SYMPTOM_COLS)
    text: Optional[str] = None             # free-text input as alternative


class PredictResponse(BaseModel):
    level: str
    confidence: float
    probabilities: dict
    active_symptoms: int
    detected_symptoms: List[str]
    hard_override: bool


def text_to_vector(text: str) -> List[int]:
    """Convert free text to symptom vector using the same logic as vectorizer.js"""
    if not SYMPTOM_COLS:
        return []
    vector = [0] * len(SYMPTOM_COLS)
    text_lower = text.lower()

    # Apply Hindi synonym map
    for hindi_word, english_symptom in SYMPTOM_MAP.items():
        if hindi_word in text_lower:
            text_lower += " " + english_symptom.replace("_", " ")

    # Match against symptom columns
    for i, symptom in enumerate(SYMPTOM_COLS):
        symptom_readable = symptom.replace("_", " ")
        if symptom_readable in text_lower or symptom in text_lower:
            vector[i] = 1

    return vector


def score_vector(vector: List[int]) -> dict:
    """Score a symptom vector and return triage level + confidence."""
    if not SYMPTOM_COLS:
        return {"level": "GREEN", "confidence": 0.5, "p_green": 0.5, "p_yellow": 0.3, "p_red": 0.2}

    active = [SYMPTOM_COLS[i] for i, v in enumerate(vector) if v == 1]
    red_score    = sum(RED_SYMPTOMS.get(s, 0) for s in active)
    yellow_score = sum(YELLOW_SYMPTOMS.get(s, 0) for s in active)
    hard_red     = any(s in HARD_RED_SIGNS for s in active)

    if hard_red or red_score >= 3:
        level = "RED"
        p_red, p_yellow, p_green = min(0.95, 0.60 + red_score * 0.05), 0.04, 0.01
    elif red_score >= 1 or yellow_score >= 4:
        level = "YELLOW" if red_score < 2 else "RED"
        p_yellow, p_red, p_green = 0.65, 0.25, 0.10
        if level == "RED":
            p_red, p_yellow, p_green = 0.70, 0.20, 0.10
    elif yellow_score >= 1 or len(active) >= 2:
        level = "YELLOW"
        p_green, p_yellow, p_red = 0.20, 0.70, 0.10
    else:
        level = "GREEN"
        p_green, p_yellow, p_red = 0.80, 0.15, 0.05

    confidence = round(max(p_green, p_yellow, p_red), 4)
    return {
        "level": level,
        "confidence": confidence,
        "p_green": round(p_green, 4),
        "p_yellow": round(p_yellow, 4),
        "p_red": round(p_red, 4),
        "active": active,
        "hard_override": hard_red,
    }


@app.get("/")
def home():
    return {"message": "GraamSehat ML Service", "status": "running", "symptoms_loaded": len(SYMPTOM_COLS)}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Build vector from input
    if req.symptoms and len(req.symptoms) == len(SYMPTOM_COLS):
        vector = req.symptoms
    elif req.text:
        vector = text_to_vector(req.text)
    else:
        return PredictResponse(
            level="GREEN", confidence=0.5,
            probabilities={"green": 0.5, "yellow": 0.3, "red": 0.2},
            active_symptoms=0, detected_symptoms=[], hard_override=False,
        )

    result = score_vector(vector)

    return PredictResponse(
        level=result["level"],
        confidence=result["confidence"],
        probabilities={
            "green":  result["p_green"],
            "yellow": result["p_yellow"],
            "red":    result["p_red"],
        },
        active_symptoms=len(result["active"]),
        detected_symptoms=result["active"],
        hard_override=result["hard_override"],
    )