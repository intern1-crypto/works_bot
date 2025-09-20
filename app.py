from flask import Flask, request, jsonify

app = Flask(__name__)

# ヘルスチェック用（ブラウザで https://xxxx.onrender.com/ → "ok"）
@app.route("/", methods=["GET"])
def health():
    return "ok", 200

# 接続確認用（GET でも 200 を返す）＆ 本番は POST を受ける
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # LINE WORKS の接続確認で使われることがある
        return "ok", 200

    # --- ここから通常の受信処理（POST想定） ---
    data = request.get_json(silent=True) or {}
    print("Incoming webhook:", data)

    # まずは 200 を即返す（タイムアウト防止）
    return "ok", 200
