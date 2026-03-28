# हाम्रो विद्यार्थी — Student Wellbeing Early Warning System

A multi-signal early warning system for Nepali schools that helps counselors identify students who may be struggling — before it becomes a crisis.

हाम्रो विद्यार्थी uses rule-based pattern detection for fast, always-available monitoring and an LLM reasoning engine for multi-signal risk assessment when deeper analysis is needed.

## Architecture

```
Frontend (React + Tailwind)  →  FastAPI Backend  →  JSON Data Layer
                                     ↓
                              Pattern Engine (pure logic)
                              NVIDIA NIM API (multi-signal AI reasoning)
```

**Pure logic** handles: consecutive low mood counters, baseline deviation, check-in frequency drops, mood trends, teacher observation correlation.

**AI reasoning** handles: multi-signal risk fusion, Nepali free-text distress detection, conversation starter generation, personalized creative tasks, parent messages.

## Quick Start

### Backend

```bash
cd backend
python3.11 -m uvicorn main:app --reload --port 8000
```

To enable AI features, create `backend/.env`:
```
NVIDIA_API_KEY=your-nvidia-nim-api-key-here
```

The system works without an API key — AI endpoints gracefully degrade to rule-based analysis.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and select a role to get started.

## Roles

- **Student** — Daily mood/energy check-in + personalized creative tasks based on interests and class
- **Teacher** — Log behavioral observations (tags + notes)
- **Counselor** — Dashboard with risk indicators, individual student profiles, AI analysis

## API Documentation

With the backend running, visit http://localhost:8000/docs for the full Swagger UI.

## Data

Seed data is in `backend/data/` as JSON files. Each student has a full profile including age, class, interests, strengths, favorite subjects, and guardian info for realistic demo purposes.

## Tech Stack

- **Frontend**: React 19, React Router, Tailwind CSS, Recharts, Lucide icons
- **Backend**: FastAPI, Pydantic, httpx
- **AI**: Kimi K2 Instruct via NVIDIA NIM API — used as a structured reasoning engine, not a chatbot
- **Data**: JSON files (trivially swappable to Postgres)
