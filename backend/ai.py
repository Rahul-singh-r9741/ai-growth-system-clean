import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not set — AI responses will fail")


BASE_URL = "https://api.groq.com/openai/v1"
CHAT_URL = f"{BASE_URL}/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "ai-growth-system/1.0"
}

# Safe, active Groq models (2025)
FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]


def _call_groq(prompt: str) -> str:
    last_error = None

    for model in FALLBACK_MODELS:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful startup growth consultant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }

            r = requests.post(
                CHAT_URL,
                headers=HEADERS,
                json=payload,
                timeout=60
            )

            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]

            last_error = f"{model} failed: {r.status_code} {r.text}"

        except Exception as e:
            last_error = f"{model} exception: {str(e)}"

    raise RuntimeError(f"All Groq models failed. Last error: {last_error}")


# ✅ THIS IS WHAT MAIN.PY IMPORTS
def get_ai_response(name, business, challenge):
    prompt = f"""
You are an AI growth consultant helping startups.

Client name: {name}
Business type: {business}
Growth challenge: {challenge}

Give a short, actionable growth plan in 5 bullet points.
"""
    return _call_groq(prompt)




