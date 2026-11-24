# CogniSphere — Government Scheme Assistant (MVP)

A hackathon-ready prototype for discovering government schemes, checking basic eligibility,
generating document checklists, and tracking an application workflow.

## What works in this MVP
- Search and browse a small **demo catalogue** of Indian schemes/scholarships.
- Enter a basic profile and receive rule-based eligibility matches with reasons.
- Generate a document checklist for a selected scheme.
- Create and update a local application-tracking record.
- Optional Gemini-powered natural-language assistant (works without an API key using a
  deterministic fallback).

> **Important:** The catalogue is illustrative demo data, not an authoritative or current
> government database. Verify all eligibility rules, dates, documents and links on the
> official portal before applying. This MVP does not submit government applications,
> store uploaded identity documents, or log in to government portals.

## Architecture
- React + Vite frontend
- Python FastAPI backend
- SQLite for local prototype tracking
- Optional Gemini API integration through `GEMINI_API_KEY`
- Designed extension points for Playwright/MCP integration; no unattended portal
  submissions are enabled in this prototype.

## Run locally

### 1. Backend
Requirements: Python 3.10+

```bash
cd backend
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

Optional Gemini setup:
- Copy `.env.example` to `.env`
- Add your Gemini API key as `GEMINI_API_KEY=...`
- Install dependencies as listed; the backend gracefully falls back if Gemini is not configured.

### 2. Frontend
Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173).

## Suggested demo flow (2–3 minutes)
1. Open the dashboard and search for "scholarship".
2. Enter a sample profile (age 19, student, Karnataka, annual family income 150000).
3. Click **Find matching schemes** and open a result.
4. Show the generated document checklist.
5. Click **Add to tracker**, then update the status to "Documents ready".
6. In the assistant, ask: "What should I prepare before applying?"

Use fictional/demo profile values during the presentation. Do not enter real Aadhaar,
bank details, passwords, or private documents.

## GitHub submission
Create a public repository named `cognisphere-government-assistant`, then from this folder:

```bash
git init
git add .
git commit -m "Build CogniSphere government scheme assistant MVP"
git branch -M main
git remote add origin https://github.com/<your-username>/cognisphere-government-assistant.git
git push -u origin main
```

Replace `<your-username>` with the GitHub account that will own the repository.

## Project structure
```text
cognisphere_mvp/
  backend/
    app/main.py
    app/data.py
    requirements.txt
    .env.example
  frontend/
    index.html
    package.json
    vite.config.js
    src/App.jsx
    src/main.jsx
    src/styles.css
  README.md
```

## Next improvements for Ideation Day
- Replace demo records with verified official scheme metadata and source timestamps.
- Add authentication and role-based access.
- Add secure document upload with consent, encryption and retention controls.
- Add OCR with user review before saving extracted fields.
- Add human-confirmed browser assistance for each supported portal.
- Add MCP tools for read-only scheme lookup and user-approved actions.
- Move SQLite to PostgreSQL and deploy frontend/backend separately.
