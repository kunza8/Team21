"""
Pure-logic pattern detection. No AI calls here — just math and counters.
These run instantly and serve as a fallback when the AI API is unreachable.
"""

from datetime import date, timedelta
from data import get_checkins, get_observations


def compute_baseline_mood(student_id: str, days: int = 30) -> float:
    checkins = get_checkins(student_id, days=days)
    if not checkins:
        return 0.0
    return round(sum(c["mood"] for c in checkins) / len(checkins), 2)


def count_consecutive_low(checkins: list[dict], threshold: int = 2) -> int:
    """Walk backwards from the most recent check-in and count how many
    in a row had mood at or below the threshold."""
    if not checkins:
        return 0

    streak = 0
    for c in reversed(checkins):
        if c["mood"] <= threshold:
            streak += 1
        else:
            break
    return streak


def compute_checkin_frequency(student_id: str) -> dict:
    """Compare check-in count in the last 7 days vs the 7 before that."""
    today = date.today()
    week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)

    checkins = get_checkins(student_id, days=30)
    recent = [c for c in checkins if c["date"] > str(week_ago)]
    previous = [c for c in checkins if str(two_weeks_ago) < c["date"] <= str(week_ago)]

    return {
        "last_7_days": len(recent),
        "previous_7_days": len(previous),
    }


def compute_mood_trend(checkins: list[dict]) -> str:
    """Simple trend: compare average of last 3 check-ins to the 3 before."""
    if len(checkins) < 4:
        return "insufficient_data"

    recent = checkins[-3:]
    earlier = checkins[-6:-3] if len(checkins) >= 6 else checkins[:-3]

    avg_recent = sum(c["mood"] for c in recent) / len(recent)
    avg_earlier = sum(c["mood"] for c in earlier) / len(earlier)

    diff = avg_recent - avg_earlier
    if diff < -0.5:
        return "declining"
    if diff > 0.5:
        return "improving"
    return "stable"


def detect_risk_level(student_id: str) -> dict:
    """Rule-based risk assessment — the fast fallback when AI is unavailable."""
    checkins = get_checkins(student_id, days=14)
    observations = get_observations(student_id)
    baseline = compute_baseline_mood(student_id)
    frequency = compute_checkin_frequency(student_id)
    consecutive_low = count_consecutive_low(checkins)
    trend = compute_mood_trend(checkins)

    recent_obs_count = len([
        o for o in observations
        if o["date"] > str(date.today() - timedelta(days=14))
    ])

    current_avg = 0.0
    if checkins:
        last_3 = checkins[-3:]
        current_avg = sum(c["mood"] for c in last_3) / len(last_3)

    baseline_deviation = baseline - current_avg if baseline else 0

    # a big frequency drop means the student stopped showing up
    freq_drop = (
        frequency["previous_7_days"] >= 5
        and frequency["last_7_days"] <= 2
    )

    risk_level = "low"
    concerns = []

    if consecutive_low >= 3 and (baseline_deviation > 2 or recent_obs_count >= 2):
        risk_level = "high"
    elif consecutive_low >= 2 or baseline_deviation > 1.5 or freq_drop:
        risk_level = "moderate"

    if consecutive_low >= 2:
        concerns.append(f"{consecutive_low} consecutive low-mood days")
    if baseline_deviation > 1:
        concerns.append(f"Mood {baseline_deviation:.1f} points below personal baseline")
    if recent_obs_count > 0:
        concerns.append(f"{recent_obs_count} teacher observation(s) in 2 weeks")
    if freq_drop:
        concerns.append("Significant drop in check-in frequency")
    if trend == "declining":
        concerns.append("Downward mood trend")

    return {
        "risk_level": risk_level,
        "consecutive_low_days": consecutive_low,
        "baseline_mood": baseline,
        "current_mood_avg": round(current_avg, 2),
        "baseline_deviation": round(baseline_deviation, 2),
        "checkin_frequency": frequency,
        "mood_trend": trend,
        "recent_observations": recent_obs_count,
        "concerns": concerns,
    }
