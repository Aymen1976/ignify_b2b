import streamlit as st
import json
import re
from pathlib import Path
from scraper import main as run_scraper
from signal_analyzer import process_file
from exporter import generate_pdf, export_csv

def clean_html(raw_html):
    """Supprime les balises HTML du résumé"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_html)

st.set_page_config(page_title="🧠 Rapport IA & Vente", layout="wide")
st.title("🧠 Rapport IA & Vente - Formateur Expert")
st.markdown("Analyse intelligente des dernières actualités en Intelligence Artificielle, spécialement pour les experts en **vente & formation**.")

if st.button("🚀 Lancer l'analyse IA"):
    with st.spinner("⏳ Collecte, analyse et génération du rapport..."):
        run_scraper()
        latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
        process_file(latest_file)

        enriched_file = sorted(Path("output").glob("analyzed_articles_*.json"))[-1]
        with open(enriched_file, "r", encoding="utf-8") as f:
            articles = json.load(f)

        st.success(f"✅ {len(articles)} articles analysés avec succès.")

        for art in articles:
            with st.container():
                st.markdown("---")
                st.markdown(f"### 📰 {art['title']}")
                st.markdown(f"**Résumé :** {clean_html(art.get('summary', 'Résumé non disponible'))}")
                st.markdown(f"**Tonalité :** `{art.get('sentiment', 'non détectée')}`")
                st.markdown(f"**Date :** {art.get('published', 'Date non précisée')}")
                st.markdown(f"[🔗 Lire l'article]({art.get('link', '#')})")

        pdf_path = generate_pdf(articles)
        csv_path = export_csv(articles)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📄 Télécharger le PDF", pdf_file, file_name=pdf_path.name)

        with open(csv_path, "rb") as csv_file:
            st.download_button("📊 Télécharger le CSV", csv_file, file_name=csv_path.name)
