from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

import os
import requests
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "llama-3.1-8b-instant"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "ai-growth-system/1.0"
}

def get_ai_response(name, business, challenge):
    if not GROQ_API_KEY:
        return "AI service is not configured. Please contact the administrator."

    prompt = f"""
You are an AI growth consultant helping startups.

Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""

    url = f"{BASE_URL}/chat/completions"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI Error: {str(e)}"
from pydantic import BaseModel
from fastapi import HTTPException

# --------- DATA MODEL ----------
class Lead(BaseModel):
    name: str
    email: str
    business: str
    challenge: str

# --------- SAFE STORAGE ----------
def save_lead_safe(lead: Lead, ai_message: str):
    try:
        # TODO: Replace this with your real DB / sheets / CRM function
        print("Saving lead:", lead.dict())
        print("AI Message:", ai_message)
        return True
    except Exception as e:
        print("Save failed, storing locally:", e)
        with open("offline_leads.txt", "a", encoding="utf-8") as f:
            f.write(f"{lead.dict()} | {ai_message}\n")
        return False

# --------- API ROUTE ----------
@app.post("/lead")
def capture_lead(lead: Lead):
    try:
        ai_message = get_ai_response(
            lead.name,
            lead.business,
            lead.challenge
        )

        success = save_lead_safe(lead, ai_message)

        return {
            "status": "success" if success else "offline",
            "ai_message": ai_message
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





