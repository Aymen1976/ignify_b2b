import httpx
import os
from dotenv import load_dotenv

# Charge correctement le fichier .env dans le dossier config/
load_dotenv(dotenv_path="config/.env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def call_mistral_raw(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-tiny",  # ou "mistral-small", "mistral-medium"
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Erreur appel Mistral :", e)
        return None

print("🔑 MISTRAL_API_KEY détectée :", MISTRAL_API_KEY)
