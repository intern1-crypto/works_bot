from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)  # デバッグ用に表示

    # 送られてきたメッセージの送信元を取得
    user = data["source"]["userId"]

    # 返信メッセージ
    response = {
        "accountId": user,
        "content": {
            "type": "text",
            "text": "お疲れ様"
        }
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
