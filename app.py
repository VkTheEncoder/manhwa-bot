import os
from flask import Flask, request
from telegram import Update
from bot import application   # your PTB Application instance
import asyncio

app = Flask(__name__)

# —— Set your Telegram webhook as soon as this module is imported
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
asyncio.run(application.bot.set_webhook(WEBHOOK_URL))

@app.route("/healthz")
def healthz():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    # queue it for the PTB Application to handle
    application.update_queue.put(update)
    return "OK"

if __name__ == "__main__":
    # for local testing, if you ever run `python app.py`
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
