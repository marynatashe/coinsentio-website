
import os
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

API_KEY = os.environ.get("ZHIPU_API_KEY")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4.7-flash"

NEWS_FILE = Path("data/news.json")
DRAFT_FILE = Path("data/drafts.json")
MAX_ARTICLES = 2


def count_chinese(text):
    return len(re.findall(r"[\u3400-\u9fff]", text))


def ask_ai(title, facts, language):
    prompt = (
        f"請根據以下已核實事實撰寫新聞。\n"
        f"語言：{language}\n"
        "正文400至600個中文字，客觀中立，"
        "使用完整段落，不得編造事實、數據或引述。"
        "不得複製原文獨特表達。"
        "只輸出正文，不要標題。\n"
        f"新聞標題：{title}\n"
        f"已核實事實：{facts}"
    )

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是 CoinSentio 的新聞編輯。"
                    "只能使用提供的已核實事實。"
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(
        request, timeout=120
    ) as response:
        result = json.loads(response.read())

    return result["choices"][0]["message"]["content"].strip()


def main():
    if not API_KEY:
        raise RuntimeError("Missing ZHIPU_API_KEY")

    news = json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    drafts = json.loads(DRAFT_FILE.read_text(encoding="utf-8"))

    existing = {item["id"] for item in drafts}
    created = 0

    for item in news:
        if created >= MAX_ARTICLES:
            break

        if item["id"] in existing:
            continue

        facts = item.get("verified_facts", "")

        # 沒有足夠的核實資料，不生成新聞
        if not isinstance(facts, str) or len(facts.strip()) < 150:
            continue

        try:
            tw = ask_ai(
                item["original_title"], facts, "繁體中文"
            )
            cn = ask_ai(
                item["original_title"], facts, "簡體中文"
            )
        except urllib.error.HTTPError as error:
            print("AI HTTP error:", error.code)
            break

        if not (
            400 <= count_chinese(tw) <= 600
            and 400 <= count_chinese(cn) <= 600
        ):
            print("Skipped article with invalid length")
            continue

        drafts.append({
            "id": item["id"],
            "source": item.get("source", ""),
            "source_url": item.get("source_url", ""),
            "original_title": item["original_title"],
            "body_tw": tw,
            "body_cn": cn,
            "status": "pending_review",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        })

        existing.add(item["id"])
        created += 1

    DRAFT_FILE.write_text(
        json.dumps(drafts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("New AI drafts:", created)


if __name__ == "__main__":
    main()
