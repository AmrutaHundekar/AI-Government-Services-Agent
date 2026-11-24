from pathlib import Path
import json
import os
import sqlite3
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .data import SCHEMES

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DB_PATH = Path(__file__).resolve().parents[1] / "cognisphere.db"

app = FastAPI(title="CogniSphere API", version="1.0.0",
              description="Hackathon MVP: scheme discovery, eligibility, checklist and tracking.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY, scheme_id TEXT NOT NULL, scheme_name TEXT NOT NULL,
            applicant_name TEXT NOT NULL, status TEXT NOT NULL,
            notes TEXT DEFAULT '', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
init_db()

class Profile(BaseModel):
    age: int = Field(ge=1, le=110)
    state: str = "Karnataka"
    annual_income: int = Field(ge=0)
    is_student: bool = False
    category: Optional[str] = None

class TrackCreate(BaseModel):
    scheme_id: str
    applicant_name: str = Field(min_length=1, max_length=80)
    notes: str = ""

class TrackUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

@app.get("/")
def home():
    return {"name": "CogniSphere API", "status": "running", "docs": "/docs"}

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/schemes")
def list_schemes(q: str = "", category: str = "All"):
    items = SCHEMES
    if category != "All":
        items = [s for s in items if s["category"].lower() == category.lower()]
    if q.strip():
        needle = q.lower().strip()
        items = [s for s in items if needle in (s["name"] + " " + s["description"] + " " + s["category"]).lower()]
    return {"items": items, "count": len(items), "notice": "Demo catalogue. Verify on official portals."}

@app.post("/api/eligibility")
def eligibility(profile: Profile):
    results = []
    for s in SCHEMES:
        reasons, warnings = [], []
        if not (s["min_age"] <= profile.age <= s["max_age"]):
            reasons.append(f"Age must be between {s['min_age']} and {s['max_age']} for this demo rule.")
        if s["max_income"] is not None and profile.annual_income > s["max_income"]:
            reasons.append(f"Demo income ceiling is ₹{s['max_income']:,} per year.")
        if s["student_required"] and not profile.is_student:
            reasons.append("This demo record is intended for students.")
        if "All India" not in s["states"] and profile.state not in s["states"]:
            reasons.append("This demo record is not listed for the selected state.")
        if not reasons:
            warnings.append("Preliminary match only. Official eligibility may include additional conditions.")
        results.append({
            "scheme": s, "eligible": len(reasons) == 0,
            "reasons": reasons, "warnings": warnings
        })
    results.sort(key=lambda x: (not x["eligible"], x["scheme"]["name"]))
    return {"matches": results, "profile_checked": True}

@app.get("/api/schemes/{scheme_id}/checklist")
def checklist(scheme_id: str):
    scheme = next((s for s in SCHEMES if s["id"] == scheme_id), None)
    if not scheme:
        raise HTTPException(404, "Scheme not found")
    return {"scheme_id": scheme_id, "scheme_name": scheme["name"],
            "documents": scheme["documents"],
            "notice": "Checklist is illustrative; confirm the current official portal requirements."}

@app.post("/api/applications")
def create_application(payload: TrackCreate):
    scheme = next((s for s in SCHEMES if s["id"] == payload.scheme_id), None)
    if not scheme:
        raise HTTPException(404, "Scheme not found")
    app_id = str(uuid.uuid4())[:8].upper()
    with db() as conn:
        conn.execute("INSERT INTO applications (id, scheme_id, scheme_name, applicant_name, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
                     (app_id, scheme["id"], scheme["name"], payload.applicant_name.strip(), "Interested", payload.notes))
    return {"id": app_id, "status": "Interested", "message": "Added to your local demo tracker."}

@app.get("/api/applications")
def get_applications():
    with db() as conn:
        rows = conn.execute("SELECT * FROM applications ORDER BY created_at DESC").fetchall()
    return {"items": [dict(r) for r in rows]}

@app.patch("/api/applications/{application_id}")
def update_application(application_id: str, payload: TrackUpdate):
    allowed = {"Interested", "Documents ready", "Application in progress", "Submitted", "Follow-up"}
    if payload.status not in allowed:
        raise HTTPException(400, f"Status must be one of: {', '.join(sorted(allowed))}")
    with db() as conn:
        row = conn.execute("SELECT id FROM applications WHERE id=?", (application_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Application record not found")
        if payload.notes is None:
            conn.execute("UPDATE applications SET status=? WHERE id=?", (payload.status, application_id))
        else:
            conn.execute("UPDATE applications SET status=?, notes=? WHERE id=?",
                         (payload.status, payload.notes, application_id))
    return {"id": application_id, "status": payload.status}

@app.post("/api/assistant")
def assistant(payload: AskRequest):
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if key:
        try:
            from google import genai
            client = genai.Client(api_key=key)
            catalogue = [{"name": s["name"], "category": s["category"], "description": s["description"]} for s in SCHEMES]
            prompt = (
                "You are CogniSphere, a cautious assistant explaining how to discover government schemes. "
                "Use only the demo catalogue context below when discussing listed schemes. "
                "Do not claim eligibility is official, do not invent deadlines or benefits, and direct users "
                "to official portals for verification. Never ask for Aadhaar, passwords, bank numbers or OTPs. "
                f"Catalogue: {json.dumps(catalogue)}\\nUser question: {payload.question}"
            )
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"), contents=prompt
            )
            return {"answer": response.text or "I could not generate a response. Please try again.", "mode": "Gemini"}
        except Exception:
            pass
    q = payload.question.lower()
    if any(word in q for word in ["document", "checklist", "prepare"]):
        answer = "Choose a scheme and open its document checklist. The list is only a starting point; confirm the latest requirements on the official portal. Avoid sharing identity numbers, OTPs or bank details here."
    elif any(word in q for word in ["eligible", "eligibility", "qualify"]):
        answer = "Use the Eligibility Checker with a sample profile. It applies simple demo rules and is not an official eligibility decision. Check the scheme's official portal before applying."
    elif any(word in q for word in ["track", "status", "application"]):
        answer = "Add a scheme to My Tracker to create a local record, then update its status as you prepare. This prototype does not connect to government application status systems."
    else:
        answer = "I can help you discover demo schemes, understand preliminary eligibility, prepare a document checklist, and organize your next steps. Search the catalogue or use the Eligibility Checker. Always verify details on official government portals."
    return {"answer": answer, "mode": "Local assistant"}
