
import json
import re
import os
import tempfile
from pathlib import Path
from datetime import datetime, timezone

INBOX = Path("incoming-news")
OUTPUT = Path("data/published_news.json")

REQUIRED = (
    "id", "title_tw", "title_cn",
    "published_at", "source"
)


def parse_markdown(text):
    text = text.lstrip("\ufeff")

    match = re.match(
        r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z",
        text,
        re.S
    )
    if not match:
        raise ValueError("Missing front matter")

    metadata = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError("Invalid metadata line")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if not key or key in metadata:
            raise ValueError("Invalid or duplicate metadata")
        metadata[key] = value

    for key in REQUIRED:
        if not metadata.get(key):
            raise ValueError("Missing field: " + key)

    if metadata.get("status", "publish") != "publish":
        raise ValueError("Article not approved for publishing")

    body = match.group(2)

    sections = re.split(
        r"(?m)^##\s+(繁體中文|简体中文)\s*$",
        body
    )

    if len(sections) != 5:
        raise ValueError("Expected two language sections")

    if sections[1] != "繁體中文" or sections[3] != "简体中文":
        raise ValueError("Wrong language section order")

    tw = sections[2].strip()
    cn = sections[4].strip()

    if not tw or not cn:
        raise ValueError("Empty article body")

    return {
        "id": metadata["id"],
        "title_tw": metadata["title_tw"],
        "title_cn": metadata["title_cn"],
        "body_tw": tw,
        "body_cn": cn,
        "category": metadata.get("category", "News"),
        "published_at": metadata["published_at"],
        "source": metadata["source"],
        "source_url": metadata.get("source_url", ""),
        "status": "published"
    }


def save_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".published-",
            suffix=".tmp",
            delete=False
        ) as temp:
            temp_name = temp.name
            json.dump(data, temp, ensure_ascii=False, indent=2)
            temp.write("\n")

        os.replace(temp_name, path)

    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def main():
    INBOX.mkdir(parents=True, exist_ok=True)

    if OUTPUT.exists():
        articles = json.loads(
            OUTPUT.read_text(encoding="utf-8")
        )
    else:
        articles = []

    if not isinstance(articles, list):
        raise ValueError("Published news must be a JSON array")

    known = {
        article["id"]
        for article in articles
    }

    imported = 0
    errors = 0

    for path in sorted(INBOX.glob("*.md")):
        try:
            article = parse_markdown(
                path.read_text(encoding="utf-8")
            )

            if article["id"] in known:
                print("Already published:", path.name)
                path.unlink()
                continue

            articles.append(article)

            # 先保存，再刪除來源
            save_json_atomic(OUTPUT, articles)

            known.add(article["id"])
            path.unlink()
            imported += 1
            print("Imported:", path.name)

        except Exception as error:
            errors += 1
            print(
                "Failed:", path.name,
                type(error).__name__, str(error)
            )

    print("New articles:", imported)
    print("Total published:", len(articles))
    print("Failed files:", errors)

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
