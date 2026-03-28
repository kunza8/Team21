"""
हाम्रो विद्यार्थी API — Student Wellbeing Early Warning System
Run with: uvicorn main:app --reload
"""

from datetime import date
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import CheckinRequest, ObservationRequest, InterventionRequest
from data import (
    get_students, get_student, get_checkins, add_checkin, get_all_checkins,
    get_observations, add_observation,
    get_interventions, add_intervention,
    get_buddy_for_student,
)
from patterns import (
    detect_risk_level, compute_baseline_mood, count_consecutive_low,
    compute_checkin_frequency, compute_mood_trend,
)
from ai import call_ai

app = FastAPI(
    title="हाम्रो विद्यार्थी API",
    description="Student wellbeing early warning system for Nepali schools",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/students")
def list_students():
    """Return every student with their computed risk snapshot."""
    students = get_students()
    result = []
    for s in students:
        checkins = get_checkins(s["id"], days=14)
        risk = detect_risk_level(s["id"])
        last_checkin = checkins[-1] if checkins else None
        result.append({
            **s,
            "last_mood": last_checkin["mood"] if last_checkin else None,
            "last_energy": last_checkin["energy"] if last_checkin else None,
            "last_checkin_date": last_checkin["date"] if last_checkin else None,
            "risk_level": risk["risk_level"],
            "concerns": risk["concerns"],
        })
    return result


@app.get("/api/students/{student_id}")
def get_student_detail(student_id: str):
    student = get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student


@app.get("/api/students/{student_id}/checkins")
def list_checkins(student_id: str, days: int = 14):
    return get_checkins(student_id, days=days)


@app.post("/api/checkins")
async def create_checkin(req: CheckinRequest):
    checkin = {
        "id": f"c-{uuid4().hex[:8]}",
        "student_id": req.student_id,
        "date": date.today().isoformat(),
        "mood": req.mood,
        "energy": req.energy,
        "note": req.note,
    }
    add_checkin(checkin)

    # run distress analysis on the note if the student wrote something
    note_analysis = None
    if req.note.strip():
        note_analysis = await call_ai("note_analysis", {"note": req.note})

    return {"checkin": checkin, "note_analysis": note_analysis}


@app.get("/api/observations/{student_id}")
def list_observations(student_id: str):
    return get_observations(student_id)


@app.post("/api/observations")
def create_observation(req: ObservationRequest):
    obs = {
        "id": f"o-{uuid4().hex[:8]}",
        "student_id": req.student_id,
        "teacher": req.teacher,
        "tags": req.tags,
        "note": req.note,
        "date": date.today().isoformat(),
    }
    add_observation(obs)
    return obs


@app.get("/api/interventions/{student_id}")
def list_interventions(student_id: str):
    return get_interventions(student_id)


@app.post("/api/interventions")
def create_intervention(req: InterventionRequest):
    intervention = {
        "id": f"i-{uuid4().hex[:8]}",
        "student_id": req.student_id,
        "counselor": req.counselor,
        "type": req.type,
        "note": req.note,
        "date": date.today().isoformat(),
        "status": req.status,
    }
    add_intervention(intervention)
    return intervention


@app.get("/api/watchlist")
def watchlist():
    """Students whose rule-based risk is moderate or higher."""
    students = get_students()
    flagged = []
    for s in students:
        risk = detect_risk_level(s["id"])
        if risk["risk_level"] in ("moderate", "high", "crisis"):
            checkins = get_checkins(s["id"], days=14)
            last = checkins[-1] if checkins else None
            flagged.append({
                **s,
                "last_mood": last["mood"] if last else None,
                "last_checkin_date": last["date"] if last else None,
                "risk": risk,
            })
    order = {"crisis": 0, "high": 1, "moderate": 2}
    flagged.sort(key=lambda f: order.get(f["risk"]["risk_level"], 3))
    return flagged


@app.post("/api/analyze/risk/{student_id}")
async def analyze_risk(student_id: str):
    student = get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    checkins = get_checkins(student_id, days=14)
    observations = get_observations(student_id)
    interventions = get_interventions(student_id)
    baseline = compute_baseline_mood(student_id)
    frequency = compute_checkin_frequency(student_id)

    # bundle every signal we have on this student for the AI to reason over
    signal_bundle = {
        "student": {"name": student["name"], "age": student["age"], "class": student["class"]},
        "mood_history": [c["mood"] for c in checkins],
        "energy_history": [c["energy"] for c in checkins],
        "notes": [{"date": c["date"], "text": c["note"]} for c in checkins if c.get("note")],
        "teacher_observations": observations,
        "checkin_frequency": frequency,
        "baseline_mood_avg": baseline,
        "days_on_watchlist": 0,
        "active_intervention": interventions[0] if interventions else None,
    }

    rule_based = detect_risk_level(student_id)
    ai_assessment = await call_ai("risk_assessment", signal_bundle)

    return {
        "student_id": student_id,
        "rule_based": rule_based,
        "ai_assessment": ai_assessment,
    }


@app.post("/api/generate/conversation-starters/{student_id}")
async def conversation_starters(student_id: str):
    student = get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    checkins = get_checkins(student_id, days=7)
    observations = get_observations(student_id)

    context = {
        "student": {"name": student["name"], "age": student["age"], "class": student["class"]},
        "recent_moods": [c["mood"] for c in checkins],
        "recent_notes": [c["note"] for c in checkins if c.get("note")],
        "observations": observations,
    }
    result = await call_ai("conversation_starters", context)
    return result


@app.get("/api/buddies/{student_id}")
def get_buddy(student_id: str):
    buddy_info = get_buddy_for_student(student_id)
    if not buddy_info:
        raise HTTPException(404, "No buddy assigned")
    return buddy_info


@app.post("/api/generate/creative-task/{student_id}")
async def creative_task(student_id: str):
    """Generate a creative activity for this student and their buddy to do together."""
    student = get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    def profile(s):
        return {
            "name": s["name"],
            "age": s["age"],
            "class": s["class"],
            "gender": s.get("gender"),
            "interests": s.get("interests", []),
            "strengths": s.get("strengths", []),
            "favorite_subjects": s.get("favorite_subjects", []),
            "struggles_with": s.get("struggles_with", []),
        }

    context = {"student": profile(student)}

    buddy_info = get_buddy_for_student(student_id)
    if buddy_info:
        context["buddy"] = profile(buddy_info["buddy"])

    result = await call_ai("creative_task", context)
    return result


@app.post("/api/generate/parent-message/{student_id}")
async def parent_message(student_id: str):
    student = get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    checkins = get_checkins(student_id, days=7)
    observations = get_observations(student_id)

    context = {
        "student": {"name": student["name"], "age": student["age"], "class": student["class"]},
        "recent_moods": [c["mood"] for c in checkins],
        "observations": observations,
    }
    result = await call_ai("parent_message", context)
    return result


@app.get("/api/class/{class_name}/trends")
def class_trends(class_name: str):
    students = [s for s in get_students() if s["class"] == class_name]
    all_checkins = get_all_checkins()

    class_student_ids = {s["id"] for s in students}
    class_checkins = [c for c in all_checkins if c["student_id"] in class_student_ids]

    if not class_checkins:
        return {"class": class_name, "student_count": len(students), "avg_mood": None}

    avg_mood = round(sum(c["mood"] for c in class_checkins) / len(class_checkins), 2)
    return {
        "class": class_name,
        "student_count": len(students),
        "avg_mood": avg_mood,
        "total_checkins": len(class_checkins),
    }
