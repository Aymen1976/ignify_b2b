from src.scraper import main as run_scraper
from src.signal_analyzer import process_file
from src.exporter import generate_pdf, export_csv
from src.mailer import send_email
from pathlib import Path
import json

def run_pipeline():
    print("Lancement du pipeline Ignify B2B - spécial veille IA")

    # Étape 1 : Scraping des flux RSS
    run_scraper()

    # Étape 2 : Analyse locale des articles
    latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
    enriched_file = process_file(latest_file)

    # Étape 3 : Chargement des articles enrichis
    with open(enriched_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("Aucun article pertinent trouvé.")
        return

    # Étape 4 : Génération du PDF et CSV
    pdf_path = generate_pdf(articles)
    csv_path = export_csv(articles)

    # Étape 5 : Envoi de l'email avec les fichiers en pièce jointe
    send_email(
        subject="Rapport quotidien - Veille IA",
        body="Bonjour,\n\nVeuillez trouver en pièce jointe le rapport quotidien sur les dernières actualités en intelligence artificielle.\n\nBien cordialement,\nL’équipe IA",
        attachments=[pdf_path, csv_path]
    )

if __name__ == "__main__":
    run_pipeline()
