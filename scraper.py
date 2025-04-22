# src/scraper.py

import feedparser
import json
from datetime import datetime, timedelta
from pathlib import Path

# Flux RSS ciblés pour l'IA
RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "https://www.aitimejournal.com/feed",
    "https://www.analyticsvidhya.com/blog/category/news/feed/",
    "https://spectrum.ieee.org/rss/artificial-intelligence"
]

# Mots-clés pour filtrer les articles IA récents et pertinents
KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "deep learning", "chatbot",
    "neural network", "transformer", "LLM", "GPT", "openai", "automation"
]

# Création du dossier output
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def is_recent(published_str):
    """Vérifie si l'article a été publié il y a moins de 48h."""
    try:
        published = datetime(*feedparser._parse_date(published_str)[:6])
        return datetime.utcnow() - published < timedelta(hours=48)
    except Exception:
        return False

def is_relevant(article):
    """Vérifie si l'article contient des mots-clés IA récents."""
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)

def parse_feed(url):
    print(f"Lecture du flux : {url}")
    feed = feedparser.parse(url)
    filtered_articles = []

    for entry in feed.entries:
        article = {
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "source": url
        }

        if is_relevant(article) and is_recent(article["published"]):
            filtered_articles.append(article)

    return filtered_articles

def save_articles(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"articles_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"{len(articles)} articles pertinents enregistrés dans {output_file}")

def main():
    all_articles = []
    for feed_url in RSS_FEEDS:
        articles = parse_feed(feed_url)
        all_articles.extend(articles)

    save_articles(all_articles)

if __name__ == "__main__":
    main()
