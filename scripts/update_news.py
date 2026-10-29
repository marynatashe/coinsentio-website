
import json
import hashlib
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEEDS = [
    {
        "name": "動區動趨",
        "language": "tw",
        "url": "https://www.blocktempo.com/feed/"
    },
    {
        "name": "PANews",
        "language": "cn",
        "url": (
            "https://www.panewslab.com/rss.xml"
            "?lang=zh&type=NORMAL"
        )
    }
]

OUTPUT = Path("data/news.json")


def read_text(element, tag):
    node = element.find(tag)
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def collect_feed(feed):
    request = urllib.request.Request(
        feed["url"],
        headers={
            "User-Agent": "CoinSentioNewsBot/1.0",
            "Accept": "application/rss+xml, application/xml"
        }
    )

    with urllib.request.urlopen(
        request, timeout=20
    ) as response:
        content = response.read()

    root = ET.fromstring(content)
    items = root.findall(".//item")
    results = []

    for item in items[:15]:
        title = read_text(item, "title")
        link = read_text(item, "link")
        date = read_text(item, "pubDate")

        if not title or not link:
            continue

        try:
            published = parsedate_to_datetime(date)
            published = published.astimezone(timezone.utc)
            date = published.isoformat()
        except (TypeError, ValueError):
            date = ""

        news_id = hashlib.sha256(
            link.encode("utf-8")
        ).hexdigest()[:16]

        results.append({
            "id": news_id,
            "source": feed["name"],
            "language": feed["language"],
            "original_title": title,
            "source_url": link,
            "published_at": date,
            "status": "collected"
        })

    return results


def main():
    OUTPUT.parent.mkdir(
        parents=True, exist_ok=True
    )

    existing = []

    if OUTPUT.exists():
        try:
            existing = json.loads(
                OUTPUT.read_text(encoding="utf-8")
            )
            if not isinstance(existing, list):
                existing = []
        except (ValueError, OSError):
            existing = []

    by_id = {
        item["id"]: item
        for item in existing
        if isinstance(item, dict) and "id" in item
    }

    for feed in FEEDS:
        try:
            items = collect_feed(feed)
            print(feed["name"], "collected:", len(items))

            for item in items:
                if item["id"] not in by_id:
                    by_id[item["id"]] = item

        except Exception as error:
            print(feed["name"], "error:", error)

    news = sorted(
        by_id.values(),
        key=lambda item: item.get("published_at", ""),
        reverse=True
    )[:200]

    OUTPUT.write_text(
        json.dumps(
            news,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("Total news:", len(news))
    print("Saved to:", OUTPUT)


if __name__ == "__main__":
    main()
