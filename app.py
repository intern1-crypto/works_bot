import os
import requests
from flask import Flask, request

app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BOT_NO = os.environ.get("BOT_NO")

TOKEN_URL = "https://auth.worksmobile.com/oauth2/v2.0/token"
SEND_URL = "https://www.worksapis.com/v1.0/bots/{bot_no}/users/{user_id}/messages"

@app.route("/", methods=["GET"])
def health():
    return "ok", 200

def get_access_token():
    """Access Token を取得"""
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "bot",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def send_message(user_id: str, text: str = "お疲れ様"):
    """ユーザーにメッセージを送信"""
    token = get_access_token()
    url = SEND_URL.format(bot_no=BOT_NO, user_id=user_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
    }
    body = {"content": {"type": "text", "text": text}}
    r = requests.post(url, headers=headers, json=body, timeout=10)
    print("send_message:", r.status_code, r.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "ok", 200

    data = request.get_json(silent=True) or {}
    print("Incoming webhook:", data)

    # ユーザーIDを取り出して返信
    user_id = (data.get("source") or {}).get("userId")
    if user_id:
        try:
            send_message(user_id, "お疲れ様")
        except Exception as e:
            print("send_message error:", e)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
