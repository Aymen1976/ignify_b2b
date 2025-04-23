import json
from datetime import datetime
from pathlib import Path

def analyze_article(article):
    """Analyse simple locale : génère un faux résumé + tonalité."""
    title = article.get("title", "Sans titre")
    summary = article.get("summary", "")
    text = f"{title}. {summary}".strip()

    # Faux résumé
    auto_summary = f"(Résumé auto) {summary[:200]}..." if summary else "(Pas de résumé disponible)"

    # Tonalité fictive simple
    sentiment = "positif" if any(word in text.lower() for word in ["improve", "growth", "progress", "innovation"]) else "neutre"

    return {
        "title": title,
        "link": article.get("link", ""),
        "published": article.get("published", ""),
        "summary": auto_summary,
        "sentiment": sentiment
    }

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    analyzed_articles = []
    for article in articles:
        print(f"Analyse de : {article.get('title', '')}")
        result = analyze_article(article)
        analyzed_articles.append(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path("output") / f"analyzed_articles_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analyzed_articles, f, indent=2, ensure_ascii=False)

    print(f"Fichier enrichi sauvegardé : {output_file}")
    return output_file
