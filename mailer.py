import smtplib
from email.message import EmailMessage
from pathlib import Path
import os
from dotenv import load_dotenv

# Charger les variables d’environnement (.env dans le dossier config/)
load_dotenv(dotenv_path=Path("config/.env"))

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body, attachments):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS  # ou l’adresse du client
    msg["Subject"] = subject
    msg.set_content(body)

    for attachment in attachments:
        path = Path(attachment)
        with open(path, "rb") as f:
            file_data = f.read()
            file_name = path.name
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name
        )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Email envoyé avec succès !")
    except Exception as e:
        print("❌ Erreur lors de l'envoi de l'email :", e)
