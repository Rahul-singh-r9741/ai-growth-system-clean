import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def _groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4,
        "max_tokens": 300
    }

    r = requests.post(url, headers=headers, json=payload, timeout=120)

    # Debug help if Groq returns an error
    if r.status_code != 200:
        raise RuntimeError(f"Groq API error {r.status_code}: {r.text}")

    return r.json()["choices"][0]["message"]["content"]


def get_ai_response(name, business, challenge):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in environment")

    prompt = f"""
Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""
    return _groq(prompt)
