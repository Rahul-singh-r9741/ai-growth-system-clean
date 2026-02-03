import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_ai_response(name, business, challenge):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY missing in environment variables")

    prompt = f"""
You are an AI growth consultant helping startups.

Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "ai-growth-system/1.0"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise RuntimeError(f"Groq error {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
