# src/exporter.py

from fpdf import FPDF
from pathlib import Path
from datetime import datetime
import pandas as pd
import unicodedata

# Classe PDF personnalisée
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Rapport de veille - Intelligence Artificielle", ln=True, align='C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", '', 11)
        self.multi_cell(0, 8, body)
        self.ln()

    def add_article(self, index, article):
        self.set_font("Arial", 'B', 12)
        title = clean_text(article.get("title", "Sans titre"))
        self.cell(0, 10, f"{index + 1}. {title}", ln=True)

        self.set_font("Arial", '', 11)
        summary = clean_text(article.get("summary", "Pas de résumé"))
        date = clean_text(article.get("published", "Date non disponible"))
        link = clean_text(article.get("link", "Lien non fourni"))
        sentiment = clean_text(article.get("sentiment", "non détecté"))

        body = (
            f"Date de publication : {date}\n"
            f"Résumé : {summary}\n"
            f"Tonalité détectée : {sentiment}\n"
            f"Lien : {link}"
        )
        self.chapter_body(body)

# Nettoyage pour éviter les erreurs d'encodage
def clean_text(text):
    if not text:
        return ""
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

# Génération du PDF
def generate_pdf(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_file = Path("output") / f"report_{timestamp}.pdf"

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for i, article in enumerate(articles):
        pdf.add_article(i, article)

    pdf.output(str(pdf_file))
    print(f"✅ PDF généré : {pdf_file}")
    return pdf_file

# Génération du CSV
def export_csv(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = Path("output") / f"report_{timestamp}.csv"

    df = pd.DataFrame(articles)
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

    print(f"✅ CSV généré : {csv_file}")
    return csv_file
