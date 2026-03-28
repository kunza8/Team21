"""
NVIDIA NIM API integration using Kimi K2 Instruct.
All AI calls funnel through call_ai(). If the API key is missing or
the model is unavailable, every endpoint gracefully degrades to
rule-based analysis.
"""

import os
import re
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_ID = "moonshotai/kimi-k2-instruct"

SYSTEM_PROMPT = """You are the AI reasoning engine for "हाम्रो विद्यार्थी", a student wellbeing \
early warning system used in Nepali schools. You are NOT a chatbot. \
You are an analytical tool that helps school counselors identify and \
support students who may be struggling.

You operate in 5 modes based on the "mode" field in the input.

MODE: "risk_assessment"
You receive a JSON object with ALL available signals for one student. \
Analyze every signal together. Return ONLY valid JSON:
{
  "risk_level": "low" | "moderate" | "high" | "crisis",
  "confidence": 0.0-1.0,
  "primary_concerns": ["1-3 key concerns"],
  "signal_summary": "2-3 sentence plain-language summary for a non-clinical counselor",
  "signal_summary_np": "Same summary in Nepali",
  "recommended_action": "Specific next step",
  "escalation_needed": true/false,
  "reasoning": "How you weighted the signals"
}
Guidelines: personal baseline drops matter more than absolute values. \
Multiple teachers flagging the same student amplifies the signal. \
Nepali distress idioms to watch for: "मलाई केही मन लाग्दैन" (apathy), \
"सबै बेकार छ" (hopelessness), "कसैले बुझ्दैन" (isolation), \
"घरमा झगडा" (family conflict), "मर्न मन लाग्छ" / "बाँच्न मन छैन" (CRISIS). \
Declining check-in frequency is itself a signal.

MODE: "note_analysis"
Analyze a single Nepali student note. Return ONLY valid JSON:
{
  "distress_detected": true/false,
  "severity": "none"|"mild"|"moderate"|"severe"|"crisis",
  "themes": ["family_conflict","academic_stress","peer_issues","loneliness","hopelessness","self_harm","anger","grief","bullying","other"],
  "key_phrases": ["relevant Nepali phrases"],
  "english_translation": "full translation",
  "requires_immediate_attention": true/false
}

MODE: "conversation_starters"
Generate 3 warm Nepali conversation openers for a counselor to check in \
with the student. Return JSON with a "starters" array of objects each having \
"nepali", "english", and "context" fields.

MODE: "creative_task"
You receive profiles for TWO students who are buddies (same class or close). \
Generate a fun, age-appropriate creative activity or mini-project that BOTH \
students can do TOGETHER this week. The task should feel collaborative and \
engaging — not homework. It should blend both students' interests and \
strengths so each person contributes something. Address them by first name.

Return ONLY valid JSON:
{
  "task_np": "The task description in Nepali, addressing both students",
  "task_en": "The task description in English, addressing both students",
  "category": "art" | "writing" | "science" | "music" | "craft" | "social" | "puzzle" | "nature" | "tech",
  "materials_needed": ["simple items needed, keep it minimal"],
  "why_this_pair": "1-sentence explaining why this task works for THIS pair",
  "bonus_challenge": "An optional stretch goal they can try together"
}

MODE: "parent_message"
Generate a brief collaborative Nepali message for a parent. Return JSON \
with "message_np", "message_en", and "tone" fields.

GLOBAL RULES:
- ALWAYS return valid JSON only. No markdown wrapping, no extra text.
- NEVER diagnose mental health conditions or recommend medication.
- If ANY input suggests self-harm, set highest severity and include: \
  "Immediate action needed. Contact 1166 helpline or take the student to the nearest health post."
- You are a support tool for human counselors, not a replacement."""


def _extract_json(text: str) -> dict:
    """Pull the first valid JSON object out of the model's response,
    ignoring any surrounding prose or markdown fencing."""
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # fallback: find the outermost { ... } or [ ... ] block
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == start_char:
                depth += 1
            elif text[i] == end_char:
                depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])

    raise ValueError("No JSON found in response")


async def call_ai(mode: str, data: dict) -> dict | None:
    """Single entry point for every AI call. Returns None when the API is unavailable."""
    if not NVIDIA_API_KEY:
        return None

    user_message = json.dumps({"mode": mode, "data": data}, ensure_ascii=False)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                NVIDIA_BASE_URL,
                headers={
                    "Authorization": f"Bearer {NVIDIA_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL_ID,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    "temperature": 0.6,
                    "top_p": 0.9,
                    "max_tokens": 2048,
                },
                timeout=120.0,
            )

        if resp.status_code != 200:
            print(f"[AI] NVIDIA NIM returned {resp.status_code}: {resp.text[:300]}")
            return None

        result = resp.json()
        text = result["choices"][0]["message"]["content"]
        return _extract_json(text)

    except Exception as e:
        print(f"[AI] NVIDIA NIM call failed ({mode}): {e}")
        return None
