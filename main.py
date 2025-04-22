# main.py

from src.scraper import main as run_scraper
from src.signal_analyzer import process_file
from src.exporter import generate_pdf, export_csv
from src.mailer import send_email
from pathlib import Path
import json

def run_pipeline():
    print("🚀 Lancement du pipeline Ignify B2B - spécial veille IA")

    # 1. Scraping ciblé IA
    run_scraper()

    # 2. Analyse IA locale
    latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
    enriched_file = process_file(latest_file)

    # 3. Lecture des articles enrichis
    with open(enriched_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # 4. Export PDF + CSV
    pdf_path = generate_pdf(articles)
    csv_path = export_csv(articles)

    # 5. Envoi e-mail automatique
    send_email(
        subject="🧠 Rapport de veille IA - Automatique",
        body="Bonjour,\n\nVeuillez trouver en pièces jointes le rapport quotidien sur les dernières actualités en Intelligence Artificielle.\n\nBien cordialement,\nL’équipe IA",
        attachments=[pdf_path, csv_path]
    )

if __name__ == "__main__":
    run_pipeline()
