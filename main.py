from src.scraper import main as run_scraper
from src.signal_analyzer import process_file
from src.exporter import generate_pdf, export_csv
from src.mailer import send_email
from pathlib import Path
import json

def run_pipeline():
    print("Lancement du pipeline Ignify B2B - spécial veille IA")

    run_scraper()

    latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
    enriched_file = process_file(latest_file)

    with open(enriched_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    pdf_path = generate_pdf(articles)
    csv_path = export_csv(articles)

    send_email(
        subject="Rapport veille IA",
        body="Voici votre rapport quotidien de veille sur l'IA.",
        attachments=[pdf_path, csv_path]
    )

if __name__ == "__main__":
    run_pipeline()
