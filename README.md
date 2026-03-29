# हाम्रो विद्यार्थी — Student Wellbeing Early Warning System

> **Catch the silence before it becomes a crisis.**

A multi-signal early warning system built for Nepali schools that detects students at risk of mental health crises — using daily check-ins, teacher observations, and AI-powered risk analysis — so counselors can intervene early, not after it's too late.

---

## The Problem

In Nepal, school counselors are responsible for hundreds of students. Mental health struggles often go unnoticed until a student drops out, self-harms, or reaches a breaking point. Teachers see warning signs daily — low energy, withdrawn behavior, falling grades — but there's no system to connect these signals into a clear picture.

**Students fall through the cracks because no one sees the full pattern.**

## Our Solution

हाम्रो विद्यार्थी turns scattered observations into actionable intelligence:

1. **Teachers log daily check-ins** — mood (1–5), energy level, and optional notes in Nepali or English
2. **Pattern engine detects warning signs** — consecutive low mood, sudden drops from baseline, missed check-ins, behavioral flags
3. **AI reasoning engine fuses multiple signals** — combines mood trends, teacher observations, peer dynamics, and free-text analysis into a unified risk score (0–100)
4. **Counselors see a prioritized dashboard** — top at-risk students, crisis alerts, class-level comparisons, and AI-generated conversation starters
5. **Interventions are tracked** — counseling sessions, parent contacts, peer support, and referrals are logged against each student

---

## Key Features

### AI-Powered Risk Intelligence
- **Risk Score (0–100)** for every student, computed from mood patterns, energy trends, observation tags, and check-in frequency
- **"Why Flagged" Explanations** — every flag comes with a human-readable reason ("3 consecutive days of mood ≤ 2", "sudden drop from baseline of 4.2")
- **AI Summary Card** — dashboard-level insights: crisis alerts needing attention, high-risk count, low mood trends, worst-performing class, watchlist status
- **Crisis Alert System** — real-time banner for keyword/pattern-detected crises with confirmation dialogs

### Multi-Role Access Control
- **Admin** — approve/reject staff registrations, assign teachers to classes
- **Teacher** — daily check-ins and observations scoped to their assigned class only
- **Counselor** — school-wide dashboard, cross-class comparison, intervention logging
- **Two-Factor Auth** — password + SMS OTP (via Twilio) for every login. Falls back to on-screen demo codes without Twilio

### Student Profile Deep Dive
- **Mood History Chart** — area chart with gradient fill showing mood trends over time
- **Collapsible Sections** — mood & energy, observations, interventions, each with visual indicators
- **Mood Emoji & Energy Color Coding** — instant visual read on student state
- **Quick Student Search** — jump to any student from the profile page
- **Print-Friendly Reports** — clean A4 output for parent meetings or case files

### Counselor Intervention Workflow
- **Log interventions directly from student profile** — counseling, parent contact, peer support, referral, or custom
- **Intervention history** tracked per student with timestamps
- **CSV Export** — download student data for offline analysis or reporting

### Full Bilingual Support (English / नेपाली)
- **170+ translated strings** covering every page, button, label, and message
- **Nepali numeral conversion** — all numbers display in Devanagari script (१, २, ३...) when in Nepali mode
- **One-click language toggle** in the sidebar

### Polished UX
- **Loading Skeletons** — smooth placeholder animations while data loads
- **Page Transitions** — fade + slide-up animations between routes
- **Toast Notifications** — contextual feedback (success, error, warning, info)
- **Keyboard Shortcuts** — `/` to search, `Esc` to navigate back
- **Empty States** — friendly illustrations when no data exists
- **Date Filtering** — filter dashboard by Today / 7 Days / 30 Days / All
- **Responsive Design** — glassmorphism sidebar with gradient accents

---

## Architecture

```
┌─────────────────────┐     ┌──────────────────────────────┐     ┌─────────────┐
│                     │     │         FastAPI Backend       │     │             │
│   React Frontend    │────▶│                              │────▶│   SQLite    │
│   (Vite + Tailwind) │     │  ┌────────────────────────┐  │     │  (SQLAlchemy)│
│                     │◀────│  │  Pattern Engine (logic) │  │     │             │
└─────────────────────┘     │  │  • Low mood streaks     │  │     └─────────────┘
                            │  │  • Baseline deviation   │  │
                            │  │  • Frequency drops      │  │
                            │  │  • Observation tags     │  │
                            │  └────────────────────────┘  │
                            │                              │
                            │  ┌────────────────────────┐  │
                            │  │  NVIDIA NIM API         │  │
                            │  │  (Kimi K2 Instruct)     │  │
                            │  │  • Multi-signal fusion  │  │
                            │  │  • Nepali text analysis │  │
                            │  │  • Risk reasoning       │  │
                            │  └────────────────────────┘  │
                            │                              │
                            │  ┌────────────────────────┐  │
                            │  │  Auth Layer             │  │
                            │  │  • JWT + bcrypt         │  │
                            │  │  • SMS OTP (Twilio)     │  │
                            │  │  • Role-based access    │  │
                            │  └────────────────────────┘  │
                            └──────────────────────────────┘
```

**Graceful Degradation**: The system works fully without an NVIDIA API key (falls back to rule-based analysis) and without Twilio (falls back to on-screen OTP codes).

---

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python3.11 seed.py          # creates SQLite DB + demo accounts
python3.11 -m uvicorn main:app --reload --port 8000
```

Create `backend/.env`:
```
NVIDIA_API_KEY=your-nvidia-nim-api-key-here
JWT_SECRET=change-this-in-production

# Twilio Verify (for real SMS OTP)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_VERIFY_SID=your-verify-service-sid
ADMIN_PHONE=+1XXXXXXXXXX
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### Demo Accounts

| Role       | Email                     | Password     | Scope       |
|------------|---------------------------|--------------|-------------|
| Admin      | admin@hamro.edu.np        | admin123     | Full access |
| Teacher    | teacher@hamro.edu.np      | teacher123   | Class 9B    |
| Counselor  | counselor@hamro.edu.np    | counselor123 | All classes |

---

## Database Schema

| Table            | Purpose                                          |
|------------------|--------------------------------------------------|
| `users`          | Auth (email, hashed password, role, status)      |
| `schools`        | School entity                                    |
| `classes`        | Grade + section                                  |
| `class_teachers` | Maps teachers to their class (N:N)               |
| `students`       | Full student profiles (interests, strengths, etc)|
| `checkins`       | Daily mood/energy logs                           |
| `observations`   | Teacher behavioral tags + notes                  |
| `interventions`  | Counselor actions logged by counselors            |
| `buddies`        | Peer buddy pairs                                 |
| `class_schedule` | Per-class timetable for time-gated check-ins     |

## Tech Stack

| Layer      | Technology                                                        |
|------------|-------------------------------------------------------------------|
| Frontend   | React 19, React Router 7, Tailwind CSS 3, Vite 6, Recharts, Lucide |
| Backend    | FastAPI, SQLAlchemy, Pydantic, httpx                              |
| Auth       | JWT (python-jose) + bcrypt (passlib) + Twilio Verify (SMS OTP)   |
| Database   | SQLite (zero config, file-based)                                  |
| AI         | Kimi K2 Instruct via NVIDIA NIM API                               |
| i18n       | Custom React context — English/Nepali with Devanagari numerals    |

## API Documentation

With the backend running, visit http://localhost:8000/docs for interactive Swagger docs.

---

## What Makes This Different

- **Not a chatbot** — AI is used as a reasoning engine to fuse signals, not to talk to students
- **Works offline from AI** — the pattern engine runs pure logic, no API dependency for core detection
- **Built for Nepal** — Nepali language support, Devanagari numerals, SMS OTP for low-connectivity environments
- **Privacy-first** — no student data leaves the school server; AI calls send only anonymized signals
- **Role-scoped by design** — teachers can't see other classes, counselors see everything, admins manage access
