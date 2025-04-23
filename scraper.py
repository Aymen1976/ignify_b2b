import feedparser
from datetime import datetime
from pathlib import Path
import json

RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "https://www.aitimejournal.com/feed",
    "https://www.analyticsvidhya.com/blog/category/news/feed/",
    "https://spectrum.ieee.org/rss/artificial-intelligence"
]

KEYWORDS = [
    "artificial intelligence", "IA", "AI", "machine learning", "deep learning",
    "chatbot", "language model", "neural network", "automation", "LLM"
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def is_relevant(article):
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)

def parse_feed(url):
    feed = feedparser.parse(url)
    return [
        {
            "title": entry.get("title", "Sans titre"),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "source": url
        }
        for entry in feed.entries if is_relevant(entry)
    ]

def main():
    all_articles = []
    for url in RSS_FEEDS:
        all_articles.extend(parse_feed(url))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"articles_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    print(f"Articles enregistrés : {len(all_articles)} dans {output_file}")
    return output_file

if __name__ == "__main__":
    main()
