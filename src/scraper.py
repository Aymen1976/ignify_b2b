import feedparser
import json
from datetime import datetime, timedelta
from pathlib import Path

# Flux RSS spécialisés IA
RSS_FEEDS = [
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
    "https://www.aitimejournal.com/feed",
    "https://www.analyticsvidhya.com/blog/category/news/feed/",
    "https://spectrum.ieee.org/rss/artificial-intelligence"
]

# Dossier de sortie
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Seuil de fraîcheur des articles (24 heures)
MAX_AGE_HOURS = 48

def is_recent(published):
    try:
        pub_date = datetime(*published[:6])
        return datetime.utcnow() - pub_date <= timedelta(hours=MAX_AGE_HOURS)
    except Exception:
        return False

def parse_feed(url):
    print(f"Lecture du flux : {url}")
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        published = entry.get("published_parsed")
        if not published or not is_recent(published):
            continue

        articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "source": url
        })

    return articles

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
