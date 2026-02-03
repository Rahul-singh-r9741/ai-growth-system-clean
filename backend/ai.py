import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def _ollama(prompt):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json().get("response")

def _groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI growth consultant for startups."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def get_ai_response(name, business, challenge):
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing in production environment")

    prompt = f"""
Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""
    return _groq(prompt)
