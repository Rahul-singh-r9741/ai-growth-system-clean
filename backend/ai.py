import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_ai_response(name, business, challenge):
    prompt = f"""
You are an AI growth consultant helping startups.

Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"]
