from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import get_ai_response
from sheets import save_lead
from emailer import send_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    name: str
    email: str
    business: str
    challenge: str

@app.post("/lead")
def capture_lead(lead: Lead):
    try:
        ai_message = get_ai_response(
            lead.name,
            lead.business,
            lead.challenge
        )
    except Exception as e:
        return {
            "status": "error",
            "stage": "ai",
            "message": str(e)
        }

    try:
        save_lead(
            lead.name,
            lead.email,
            lead.business,
            lead.challenge,
            ai_response=ai_message
        )
    except Exception as e:
        return {
            "status": "error",
            "stage": "sheets",
            "message": str(e),
            "ai_message": ai_message
        }

    try:
        send_email(
            lead.email,
            lead.name,
            ai_message
        )
    except Exception as e:
        return {
            "status": "error",
            "stage": "email",
            "message": str(e),
            "ai_message": ai_message
        }

    return {
        "status": "success",
        "message": ai_message
    }

@app.get("/health")
def health():
    return {"status": "ok"}

