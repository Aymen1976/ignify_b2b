import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Veille IA", layout="wide")
st.title("Veille sur l’intelligence artificielle")

output_dir = Path("output")
files = sorted(output_dir.glob("analyzed_articles_*.json"), reverse=True)

if not files:
    st.warning("Aucun article disponible.")
else:
    latest_file = files[0]
    with open(latest_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    st.subheader(f"{len(articles)} articles disponibles")

    for article in articles:
        with st.expander(article.get("title", "Sans titre")):
            st.write("Résumé :", article.get("summary", "Aucun résumé"))
            st.write("Date :", article.get("published", "Non précisée"))
            st.write("Tonalité :", article.get("sentiment", "Non détectée"))
            st.markdown(f"[Lire l'article]({article.get('link', '#')})")
