from src.scraper import main as run_scraper
from src.analyzer import analyze_articles
from src.exporter import generate_pdf, export_csv
from src.mailer import send_email
from pathlib import Path
import json

def run_pipeline():
    print("Lancement du pipeline Ignify B2B - spécial veille IA")

    # Étape 1 : Scraping
    run_scraper()

    # Étape 2 : Analyse IA locale
    latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
    analyzed_file = analyze_articles(latest_file)

    # Étape 3 : Chargement des articles enrichis
    with open(analyzed_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Étape 4 : Génération PDF / CSV
    pdf_path = generate_pdf(articles)
    csv_path = export_csv(articles)

    # Étape 5 : Envoi de l'e-mail
    send_email(
        subject="Rapport IA – Veille Intelligence Artificielle",
        body="Bonjour,\n\nVeuillez trouver ci-joint le dernier rapport IA.\n\nCordialement,\nL’équipe IA.",
        attachments=[pdf_path, csv_path]
    )

if __name__ == "__main__":
    run_pipeline()
