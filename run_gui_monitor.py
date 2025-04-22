# run_gui_monitor.py

import streamlit as st
from src.scraper import main as run_scraper
from src.signal_analyzer import process_file
from src.exporter import generate_pdf, export_csv
import json
from pathlib import Path

st.set_page_config(page_title="Surveillance IA & Vente", layout="centered")
st.title("📡 Surveillance des News IA récentes")
st.markdown("Surveillez automatiquement les **dernières actualités** sur l'intelligence artificielle appliquée à la vente.")

# Bouton de lancement
if st.button("🟢 Lancer la surveillance maintenant"):
    with st.spinner("🔍 Analyse en cours..."):
        run_scraper()

        # Récupérer le dernier fichier
        latest_file = sorted(Path("output").glob("articles_*.json"))[-1]
        enriched_file = process_file(latest_file)

        # Charger les articles analysés
        with open(enriched_file, "r", encoding="utf-8") as f:
            articles = json.load(f)

        # Générer les fichiers finaux
        pdf_path = generate_pdf(articles)
        csv_path = export_csv(articles)

        st.success(f"✅ {len(articles)} articles analysés et enrichis.")
        st.download_button("📄 Télécharger le PDF", data=open(pdf_path, "rb"), file_name=pdf_path.name)
        st.download_button("📊 Télécharger le CSV", data=open(csv_path, "rb"), file_name=csv_path.name)

        # Affichage détaillé
        st.markdown("---")
        st.markdown("### 🗂️ Résumés des articles IA")
        for article in articles:
            with st.expander(article["title"]):
                st.write(f"**Résumé :** {article.get('summary', '')}")
                st.write(f"**Tonalité :** {article.get('sentiment', '')}")
                st.write(f"**Date :** {article.get('published', 'Non précisée')}")
                st.markdown(f"[🔗 Lire l'article]({article['link']})")

else:
    st.warning("Appuie sur le bouton ci-dessus pour surveiller les dernières publications sur l'IA.")
