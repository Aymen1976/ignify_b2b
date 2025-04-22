# src/exporter.py

from fpdf import FPDF
import pandas as pd
from datetime import datetime
from pathlib import Path
import unicodedata

def clean_text(text):
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Rapport de veille IA", ln=True, align='C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Arial", '', 11)
        self.multi_cell(0, 8, body)
        self.ln()

    def add_article(self, index, article):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, f"{index+1}. {clean_text(article.get('title', ''))}", ln=True)
        self.set_font("Arial", '', 11)

        content = (
            f"Date : {article.get('published')}\n"
            f"Score de pertinence : {article.get('heat_score')}/10\n"
            f"Résumé : {clean_text(article.get('summary'))}\n"
            f"Lien : {article.get('link')}\n"
        )
        self.chapter_body(content)

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

def export_csv(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = Path("output") / f"report_{timestamp}.csv"
    df = pd.DataFrame(articles)
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✅ CSV généré : {csv_file}")
    return csv_file
