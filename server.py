import os
from flask import Flask, request
import requests
from openai import OpenAI

BOT = os.environ.get("BOT_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_KEY)

@app.route("/webhook", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def hook():
    data = request.get_json(force=True)

    if "message" not in data:
        return "ok"

    msg = data["message"]

    if "text" not in msg:
        return "ok"

    chat = msg["chat"]["id"]
    text = msg["text"]

    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": text}]
        )
        reply = res.choices[0].message.content
    except Exception as e:
        reply = "AI error: " + str(e)

    requests.post(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        json={"chat_id": chat, "text": reply}
    )

    return "ok"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
