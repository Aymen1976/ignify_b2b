import os
from dotenv import load_dotenv

load_dotenv()

print("📧 Adresse e-mail :", os.getenv("EMAIL_ADDRESS"))
print("🔐 Mot de passe :", "✅ OK" if os.getenv("EMAIL_PASSWORD") else "❌ Manquant")

from src.mailer import send_email

send_email(
    subject="✅ Test d’envoi Ignify",
    body="Ceci est un test simple sans pièce jointe.\n\nSi tu lis ce mail, c’est que tout fonctionne !",
    attachments=[]
)

from src.mailer import send_email

send_email(
    subject="✅ Test d’envoi Ignify",
    body="Ceci est un test simple sans pièce jointe.\n\nSi tu lis ce mail, c’est que tout fonctionne !",
    attachments=[]
)
