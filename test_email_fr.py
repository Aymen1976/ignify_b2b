from src.mailer import send_email
from fpdf import FPDF
from pathlib import Path

# Génération d'un vrai fichier PDF
pdf_path = Path("output/report_test.pdf")
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Ceci est un rapport test généré par FPDF.", ln=True, align='L')
pdf.output(str(pdf_path))

# Génération d'un fichier CSV test
csv_path = Path("output/report_test.csv")
csv_path.write_text("titre,summary,sentiment\nTest,Résumé fictif,positif", encoding="utf-8")

# Envoi de l'e-mail
send_email(
    subject="🧠 Rapport test Ignify B2B",
    body="Bonjour,\n\nCeci est un test d’envoi automatique du rapport IA.\n\nBien cordialement,\nL’équipe IA",
    attachments=[pdf_path, csv_path]
)
