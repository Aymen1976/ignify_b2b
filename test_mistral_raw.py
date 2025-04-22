from src.mistral_raw import call_mistral_raw

prompt = "Explique en 2 phrases ce qu'est l'intelligence artificielle."
response = call_mistral_raw(prompt)

print("\n🧠 Réponse Mistral :\n")
print(response)
