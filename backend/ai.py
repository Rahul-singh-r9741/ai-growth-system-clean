import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "ai-growth-system/1.0"
}

def _get_active_model():
    url = f"{BASE_URL}/models"
    r = requests.get(url, headers=HEADERS, timeout=30)

    if r.status_code != 200:
        raise RuntimeError(f"Failed to fetch Groq models: {r.text}")

    models = r.json().get("data", [])

    if not models:
        raise RuntimeError("No active Groq models available")

    # Prefer chat-capable models with large context
    for m in models:
        name = m.get("id", "")
        if "it" in name or "chat" in name or "instruct" in name:
            return name

    return models[0]["id"]


def _groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"]



