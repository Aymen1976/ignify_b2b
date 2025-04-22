from mistralai.client import MistralClient
from mistralai.models.chat import ChatMessage
from src.config import MISTRAL_API_KEY

client = MistralClient(api_key=MISTRAL_API_KEY)

def analyze_with_mistral(prompt):
    try:
        response = client.chat(
            model="mistral-tiny",  # tu peux aussi tester "mistral-small" ou "mistral-medium"
            messages=[ChatMessage(role="user", content=prompt)]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Erreur Mistral :", e)
        return None
