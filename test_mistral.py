from mistralai.client import MistralClient
from mistralai.models.chat import ChatMessage
from src.config import MISTRAL_API_KEY

client = MistralClient(api_key=MISTRAL_API_KEY)

def analyze_with_mistral(prompt):
    try:
        messages = [ChatMessage(role="user", content=prompt)]
        response = client.chat(model="mistral-tiny", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Erreur Mistral :", e)
        return None
