import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def save_lead(name, email, business, challenge):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("AI_LeADS").sheet1

    sheet.append_row([
        str(datetime.now()),
        name,
        email,
        business,
        challenge,
        "Local AI Bot"
    ])
