# src/scraper.py

import feedparser
import json
from datetime import datetime, timedelta
from pathlib import Path

# Liste des flux RSS IA spécialisés
RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "https://www.aitimejournal.com/feed",
    "https://www.analyticsvidhya.com/blog/category/news/feed/",
    "https://spectrum.ieee.org/rss/artificial-intelligence",
]

# Mots-clés IA pertinents
KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning", "neural network",
    "chatbot", "openai", "llm", "gpt", "generative ai", "automation"
]

# Dossier de sortie
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Choix de la fenêtre de temps (24 ou 48 heures)
HOURS_LIMIT = 48

def is_recent(published_str):
    try:
        published_time = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %z")
        now = datetime.now(published_time.tzinfo)
        return (now - published_time) <= timedelta(hours=HOURS_LIMIT)
    except Exception:
        return False  # Ignore les dates invalides

def is_relevant(article):
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    return any(keyword in text for keyword in KEYWORDS)

def parse_feed(url):
    print(f"📡 Lecture du flux : {url}")
    feed = feedparser.parse(url)
    filtered_articles = []

    for entry in feed.entries:
        published = entry.get("published", "")
        if not is_recent(published):
            continue

        article = {
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": published,
            "summary": entry.get("summary", ""),
            "source": url
        }

        if is_relevant(article):
            filtered_articles.append(article)

    return filtered_articles

def save_articles(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"articles_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(articles)} articles pertinents enregistrés dans {output_file}")

def main():
    all_articles = []
    for feed_url in RSS_FEEDS:
        articles = parse_feed(feed_url)
        all_articles.extend(articles)

    save_articles(all_articles)

if __name__ == "__main__":
    main()
