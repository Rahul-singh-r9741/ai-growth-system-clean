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
    ai_message = get_ai_response(
        lead.name,
        lead.business,
        lead.challenge
    )

    save_lead(
        lead.name,
        lead.email,
        lead.business,
        lead.challenge
    )

    send_email(
        lead.email,
        lead.name,
        ai_message
    )

    return {
        "status": "success",
        "message": ai_message
    }
@app.get("/health")
def health():
    return {"status": "ok"}

