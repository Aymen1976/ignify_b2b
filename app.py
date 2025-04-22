import streamlit as st
import json
from pathlib import Path
from src.scraper import main as run_scraper
from src.signal_analyzer import process_file
from src.exporter import generate_pdf, export_csv

st.set_page_config(
    page_title="🧠 Rapport IA & Vente",
    layout="wide"
)

st.title("🧠 Rapport IA & Vente - Formateur Expert")
st.markdown("**Analyse automatisée de l'actualité sur l'intelligence artificielle et la vente.**")

if st.button("🚀 Lancer le pipeline IA"):
    with st.spinner("🔎 Collecte et analyse en cours..."):
        run_scraper()
        latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
        process_file(latest_file)

        enriched_file = sorted(Path("output").glob("analyzed_articles_*.json"))[-1]
        with open(enriched_file, "r", encoding="utf-8") as f:
            articles = json.load(f)

        st.success(f"✅ {len(articles)} articles analysés avec succès.")

        # Affichage des articles
        for art in articles:
            with st.expander(f"📌 {art['title']}"):
                st.markdown(f"**Résumé :** {art.get('summary', 'Aucun résumé')}")
                st.markdown(f"**Tonalité :** {art.get('sentiment', 'Indéterminée')}")
                st.markdown(f"**Date :** {art.get('published', 'Non précisée')}")
                st.markdown(f"🔗 [Lire l'article]({art.get('link', '#')})")

        # Exports
        pdf_path = generate_pdf(articles)
        csv_path = export_csv(articles)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📄 Télécharger le rapport PDF", pdf_file, file_name=pdf_path.name)

        with open(csv_path, "rb") as csv_file:
            st.download_button("📊 Télécharger le rapport CSV", csv_file, file_name=csv_path.name)
