import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def _load_google_creds():
    raw = os.getenv("GOOGLE_CREDENTIALS")

    if not raw:
        raise RuntimeError("GOOGLE_CREDENTIALS not set")

    # If Railway mounted it as a file
    if os.path.exists(raw):
        with open(raw, "r") as f:
            return json.load(f)

    # Otherwise assume it's raw JSON text
    return json.loads(raw)

def save_lead(name, email, business, challenge, ai_response):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = _load_google_creds()
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("AI_LeADS").sheet1

    sheet.append_row([
        name,
        email,
        business,
        challenge,
        ai_response
    ])
