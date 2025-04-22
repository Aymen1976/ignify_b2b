# streamlit_app.py

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Veille IA & Vente",
    layout="wide",
)

st.title("📊 Veille sur l’Intelligence Artificielle pour la Vente")

# Récupérer le fichier JSON le plus récent
output_dir = Path("output")
files = sorted(output_dir.glob("analyzed_articles_*.json"), reverse=True)

if not files:
    st.warning("Aucun fichier d’analyse trouvé.")
else:
    with open(files[0], "r", encoding="utf-8") as f:
        articles = json.load(f)

    st.subheader(f"🗂️ Articles récents ({len(articles)} trouvés)")
    for article in articles:
        with st.expander(article.get("title", "Sans titre")):
            st.write("**Résumé :**", article.get("summary", "Aucun résumé"))
            st.write("**Date :**", article.get("published", "Inconnue"))
            st.write("**Tonalité :**", article.get("sentiment", "Non détectée"))
            st.write("[🔗 Voir l'article]({})".format(article.get("link", "#")))
