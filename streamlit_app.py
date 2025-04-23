# streamlit_app.py

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from src.exporter import export_csv, generate_filtered_pdf

st.set_page_config(
    page_title="Veille IA & Vente",
    layout="wide",
)

st.title("Veille sur l’Intelligence Artificielle appliquée à la Vente")

# Charger les articles analysés
output_dir = Path("output")
files = sorted(output_dir.glob("analyzed_articles_*.json"), reverse=True)

if not files:
    st.warning("Aucun fichier d’analyse trouvé.")
else:
    with open(files[0], "r", encoding="utf-8") as f:
        articles = json.load(f)

    st.subheader(f"Articles récents ({len(articles)} trouvés)")

    # Filtrage
    sentiments = list(set([article.get("sentiment", "non détecté") for article in articles]))
    selected_sentiments = st.multiselect("Filtrer par tonalité :", sentiments, default=sentiments)

    search_term = st.text_input("Filtrer par mot-clé (titre ou résumé) :", "")

    filtered_articles = []
    for article in articles:
        sentiment_match = article.get("sentiment") in selected_sentiments
        keyword_match = search_term.lower() in article.get("title", "").lower() or search_term.lower() in article.get("summary", "").lower()
        if sentiment_match and (search_term == "" or keyword_match):
            filtered_articles.append(article)

    st.success(f"{len(filtered_articles)} article(s) affiché(s) après filtrage.")

    # Affichage des articles
    for article in filtered_articles:
        with st.expander(article.get("title", "Sans titre")):
            st.write("Résumé :", article.get("summary", "Aucun résumé"))
            st.write("Date :", article.get("published", "Inconnue"))
            st.write("Tonalité :", article.get("sentiment", "Non détectée"))
            st.markdown(f"[🔗 Lire l'article]({article.get('link', '#')})")

    # Boutons de téléchargement
    if filtered_articles:
        if st.button("📄 Générer le PDF filtré"):
            pdf_path = generate_filtered_pdf(filtered_articles, filename="filtered_report.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le PDF",
                    data=f,
                    file_name=pdf_path.name,
                    mime="application/pdf"
                )

        if st.button("📊 Générer le CSV filtré"):
            csv_path = export_csv(filtered_articles, filename="filtered_report.csv")
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le CSV",
                    data=f,
                    file_name=csv_path.name,
                    mime="text/csv"
                )
