"""
Thin JSON-file data layer. Every read/write goes through here,
so swapping to a real DB later is just replacing these functions.
"""

import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).parent / "data"


def _read(filename: str) -> list:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def _write(filename: str, data: list):
    with open(DATA_DIR / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_students() -> list[dict]:
    return _read("students.json")


def get_student(student_id: str) -> dict | None:
    for s in get_students():
        if s["id"] == student_id:
            return s
    return None


def get_all_checkins() -> list[dict]:
    return _read("checkins.json")


def get_checkins(student_id: str, days: int | None = None) -> list[dict]:
    all_checkins = _read("checkins.json")
    filtered = [c for c in all_checkins if c["student_id"] == student_id]
    filtered.sort(key=lambda c: c["date"])

    if days:
        filtered = filtered[-days:]

    return filtered


def add_checkin(checkin: dict):
    data = _read("checkins.json")
    data.append(checkin)
    _write("checkins.json", data)


def get_observations(student_id: str | None = None) -> list[dict]:
    data = _read("observations.json")
    if student_id:
        data = [o for o in data if o["student_id"] == student_id]
    data.sort(key=lambda o: o["date"], reverse=True)
    return data


def add_observation(obs: dict):
    data = _read("observations.json")
    data.append(obs)
    _write("observations.json", data)


def get_interventions(student_id: str | None = None) -> list[dict]:
    data = _read("interventions.json")
    if student_id:
        data = [i for i in data if i["student_id"] == student_id]
    data.sort(key=lambda i: i["date"], reverse=True)
    return data


def add_intervention(intervention: dict):
    data = _read("interventions.json")
    data.append(intervention)
    _write("interventions.json", data)


def get_buddy_for_student(student_id: str) -> dict | None:
    for b in _read("buddies.json"):
        if b["student_id"] == student_id:
            buddy = get_student(b["buddy_id"])
            if buddy:
                return {"buddy": buddy, "assigned_date": b["assigned_date"]}
    return None
