from pydantic import BaseModel
from typing import Literal


class CheckinRequest(BaseModel):
    student_id: str
    mood: int
    energy: Literal["low", "medium", "high"]
    note: str = ""


class ObservationRequest(BaseModel):
    student_id: str
    teacher: str
    tags: list[str]
    note: str = ""


class InterventionRequest(BaseModel):
    student_id: str
    counselor: str
    type: str
    note: str
    status: str = "in_progress"


class RiskAssessment(BaseModel):
    risk_level: Literal["low", "moderate", "high", "crisis"]
    confidence: float
    primary_concerns: list[str]
    signal_summary: str
    signal_summary_np: str = ""
    recommended_action: str
    escalation_needed: bool
    reasoning: str


class NoteAnalysis(BaseModel):
    distress_detected: bool
    severity: Literal["none", "mild", "moderate", "severe", "crisis"]
    themes: list[str]
    key_phrases: list[str]
    english_translation: str
    requires_immediate_attention: bool
