# src/signal_analyzer.py

import json
from datetime import datetime
from pathlib import Path

def analyze_article(article):
    title = article.get("title", "")
    summary = article.get("summary", "")
    return {
        "title": title,
        "link": article.get("link"),
        "published": article.get("published", ""),
        "summary": f"(Résumé) {summary[:200]}...",
        "sentiment": "neutre",
        "heat_score": article.get("heat_score", 0)
    }

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    analyzed = []
    for article in articles:
        print(f"🧠 Article analysé : {article.get('title')}")
        result = analyze_article(article)
        analyzed.append(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path("output") / f"analyzed_articles_{timestamp}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analyzed, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier enrichi sauvegardé : {output_path}")
    return output_path
