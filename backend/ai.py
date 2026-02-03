import os
import requests

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




