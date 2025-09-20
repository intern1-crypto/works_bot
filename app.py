import os, traceback
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
    # 起動確認ログ（バージョン印字）
    print("boot: app is running, BOT_NO=", BOT_NO, "CLIENT_ID set:", bool(CLIENT_ID))
    return "ok", 200

def get_access_token():
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
    print("token resp:", resp.status_code, resp.text[:300])  # ★ 追加（本文を見る）
    resp.raise_for_status()
    return resp.json().get("access_token")

def send_message(user_id: str, text: str = "お疲れ様"):
    print("send_message: start ->", user_id)
    token = get_access_token()
    url = SEND_URL.format(bot_no=BOT_NO, user_id=user_id)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
    }
    body = {"content": {"type": "text", "text": text}}
    r = requests.post(url, headers=headers, json=body, timeout=10)
    print("send_message: done", r.status_code, r.text[:200])

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "ok", 200

    data = request.get_json(silent=True) or {}
    print("Incoming webhook:", data)

    user_id = (data.get("source") or {}).get("userId")
    if user_id:
        try:
            send_message(user_id, "お疲れ様")
        except Exception as e:
            print("send_message error:", e)
            traceback.print_exc()

    return "ok", 200
