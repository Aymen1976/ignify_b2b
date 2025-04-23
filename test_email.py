from src.mailer import send_email
from pathlib import Path
from fpdf import FPDF

# Assurer que le dossier 'output/' existe
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

# Génération d'un fichier PDF test
pdf_path = output_dir / "report_test.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Ceci est un rapport test généré automatiquement.", ln=True)
pdf.output(str(pdf_path))

# Génération d'un fichier CSV test
csv_path = output_dir / "report_test.csv"
csv_path.write_text("titre,resume,sentiment\nTest,Tout est ok,neutre", encoding="utf-8")

# Envoi de l'e-mail
send_email(
    subject="Test de rapport IA - Ignify",
    body="Ceci est un test automatique. Le mail contient un PDF et un CSV fictif.",
    attachments=[pdf_path, csv_path]
)
