# src/signal_analyzer.py

import json
from datetime import datetime
from pathlib import Path

def analyze_article(article):
    """Analyse simple locale : résumé tronqué + tonalité neutre."""
    title = article.get("title", "Sans titre")
    summary = article.get("summary", "")
    text = f"{title}. {summary}"

    # Résumé automatique basique
    resume = f"(Résumé automatique) {summary[:200]}..." if summary else "Pas de résumé disponible"
    sentiment = "neutre"  # Placeholder pour de futures améliorations

    return {
        "title": title,
        "link": article.get("link"),
        "summary": resume,
        "sentiment": sentiment,
        "published": article.get("published", "Date non disponible")
    }

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    analyzed_articles = []
    for article in articles:
        print(f"Article analysé : {article.get('title')}")
        result = analyze_article(article)
        if result:
            analyzed_articles.append(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path("output") / f"analyzed_articles_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analyzed_articles, f, indent=2, ensure_ascii=False)

    print(f"Fichier enrichi sauvegardé : {output_file}")
    return output_file
