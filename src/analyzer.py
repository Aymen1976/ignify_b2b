import json
from pathlib import Path
from datetime import datetime
from textblob import TextBlob

def analyze_article(article):
    title = article.get("title", "")
    summary = article.get("summary", "")
    full_text = f"{title}. {summary}"

    # Analyse de tonalité locale
    polarity = TextBlob(full_text).sentiment.polarity
    if polarity > 0.1:
        sentiment = "positif"
    elif polarity < -0.1:
        sentiment = "négatif"
    else:
        sentiment = "neutre"

    return {
        "title": title,
        "summary": summary,
        "published": article.get("published", ""),
        "link": article.get("link", ""),
        "sentiment": sentiment
    }

def analyze_articles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    results = []
    for article in articles:
        print("Analyse de :", article.get("title"))
        result = analyze_article(article)
        results.append(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path("output") / f"analyzed_articles_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Fichier enrichi sauvegardé : {output_file}")
    return output_file
