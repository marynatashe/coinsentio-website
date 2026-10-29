
import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("ZHIPU_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "ZHIPU_API_KEY is missing"
    )

API_URL = (
    "https://open.bigmodel.cn"
    "/api/paas/v4/chat/completions"
)

payload = {
    "model": "glm-4.7-flash",
    "messages": [
        {
            "role": "system",
            "content": (
                "你是 CoinSentio 的中文新聞編輯。"
                "使用客觀、中立的新聞語言。"
            )
        },
        {
            "role": "user",
            "content": (
                "請用繁體中文寫一句話，"
                "確認 CoinSentio AI 新聞系統"
                "已成功連接。不要編造新聞。"
            )
        }
    ],
    "temperature": 0.2,
    "max_tokens": 150
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

try:
    with urllib.request.urlopen(
        request, timeout=90
    ) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    answer = result["choices"][0]["message"]["content"]

    print("CoinSentio AI connection: SUCCESS")
    print("Model: glm-4.7-flash")
    print("AI response:")
    print(answer)


except urllib.error.HTTPError as error:
    print("AI request failed")
    print("HTTP status:", error.code)

    try:
        details = json.loads(
            error.read().decode("utf-8")
        )
        info = details.get("error", details)

        if isinstance(info, dict):
            print("Error code:", info.get("code"))
            print("Error message:", info.get("message"))
        else:
            print("Error details:", str(info)[:300])

    except Exception:
        print("Unable to decode API error")

    raise SystemExit(1)

except Exception as error:
    print("Connection error:", type(error).__name__)
    raise SystemExit(1)
