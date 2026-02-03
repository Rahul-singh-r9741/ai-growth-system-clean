import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()


def send_email(to_email, name, ai_message):
    msg = MIMEText(f"""
Hi {name},

Thanks for reaching out!

Here’s a personalized AI growth plan for you:

{ai_message}

If you'd like a walkthrough, just reply to this email.

Best,
Rahul
""")

    msg["Subject"] = "Your AI Growth Plan"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )
        server.send_message(msg)
