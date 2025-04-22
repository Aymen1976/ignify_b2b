# src/dashboard.py

import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Ignify B2B - Dashboard", layout="wide")
st.title("📊 Ignify B2B – Résumés IA des actualités B2B")

# Récupérer les fichiers analysés
files = sorted(Path("output").glob("analyzed_articles_*.json"), reverse=True)

if not files:
    st.warning("Aucun fichier d’articles enrichi trouvé dans le dossier /output.")
else:
    selected_file = st.selectbox("📁 Sélectionner un fichier d’analyse :", files)

    with open(selected_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Filtres
    sentiments = ["positif", "neutre", "négatif"]
    selected_sentiments = st.multiselect("🧠 Filtrer par sentiment :", sentiments, default=sentiments)

    # Affichage des articles
    for article in articles:
        sentiment = article.get("gpt_sentiment", "inconnu")
        if sentiment in selected_sentiments:
            st.subheader(article.get("title", "Sans titre"))
            st.markdown(f"📝 **Résumé GPT :** {article.get('gpt_summary', 'Aucun résumé')}")
            st.markdown(f"🔗 [Lire l'article]({article.get('link')})")
            st.caption(f"🕒 {article.get('published', 'Date inconnue')} | 📍 Sentiment : **{sentiment}**")
            st.divider()
