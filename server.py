import os
from flask import Flask, request
import requests
from openai import OpenAI

BOT = os.environ.get("BOT_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_KEY)

@app.route("/webhook", methods=["POST"])
def hook():
    data = request.json
    chat = data["message"]["chat"]["id"]
    msg = data["message"]["text"]

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":msg}]
    )

    reply = res.choices[0].message.content

    requests.post(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        json={"chat_id":chat,"text":reply}
    )
    return "ok"
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
