import json
import requests
import schedule
import time
import threading
from flask import Flask, request
from datetime import datetime, date

app = Flask(__name__)

# === あなたのLINE Botの情報 ===
CHANNEL_ACCESS_TOKEN = "9pIuXaVyw6sH5wHbQGADMZ9/hv1M6NT1kYsoy8QltOpol7Bjoky3TER+VYqNSxCEsG2V0/w6neXezX2M+Ubp5h8j29SjlUx/w6yT3T0NNZ31W+JeDRsAPVQDnivk8GL4qRKVC2/SO50Qp7XdVmu5mwdB04t89/1O/w1cDnyilFU="
GROUP_ID = "C33e7521b4b00dbfc378371c459e73c7d"  # 初回はイベントログから取得

# === Flask: LINE webhook受け取り ===
@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_data(as_text=True)
    print("=== Webhook受信 ===")
    print(body)

    try:
        events = json.loads(body).get("events", [])
        for event in events:
            source = event.get("source", {})
            if source.get("type") == "group":
                print("📌 受信グループID:", source.get("groupId"))
    except Exception as e:
        print("解析エラー:", e)

    return "OK", 200

# === リマインダー送信関数 ===
def send_reminder():
    print("🔔 18:00 リマインダー送信中...")
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": GROUP_ID,
        "messages": [
            {
                "type": "text",
                "text": ""
            }
        ]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
    print(f"送信結果: {response.status_code} {response.text}")

# === スケジューラを別スレッドで動かす ===
def run_schedule():
    schedule.every().day.at("19:29").do(send_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

# === メイン実行 ===
if __name__ == "__main__":
    # スケジューラを並列実行
    threading.Thread(target=run_schedule, daemon=True).start()

    # Flaskサーバーを起動（LINE Webhook用）
    app.run(port=5000)
