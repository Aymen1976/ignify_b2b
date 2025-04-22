# src/scraper.py

import feedparser
import json
from datetime import datetime
from pathlib import Path

# Flux RSS spécialisés IA
RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "https://www.aitimejournal.com/feed",
    "https://www.analyticsvidhya.com/blog/category/news/feed/",
    "https://spectrum.ieee.org/rss/artificial-intelligence",
]

# Mots-clés pour scorer la pertinence
KEYWORDS = [
    "AI", "artificial intelligence", "deep learning", "machine learning", "generative AI",
    "large language model", "transformer", "LLM", "chatbot", "GPT", "neural network",
    "autonomous", "algorithm", "prompt", "training data", "AI news", "AI model", "AI breakthrough"
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def compute_heat_score(text):
    text = text.lower()
    return sum(1 for kw in KEYWORDS if kw.lower() in text)

def parse_feed(url):
    print(f"📡 Lecture du flux : {url}")
    feed = feedparser.parse(url)
    scored_articles = []

    for entry in feed.entries:
        content = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
        score = compute_heat_score(content)

        if score > 0:
            scored_articles.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "heat_score": score,
                "source": url
            })

    return scored_articles

def save_articles(articles):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"articles_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(articles)} articles enregistrés dans {output_file}")

def main():
    all_articles = []
    for url in RSS_FEEDS:
        all_articles.extend(parse_feed(url))

    all_articles.sort(key=lambda x: x["heat_score"], reverse=True)
    save_articles(all_articles)

if __name__ == "__main__":
    main()
