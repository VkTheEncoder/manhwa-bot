import os
from flask import Flask, request
from telegram import Update
from bot import application  # your Application instance

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    # put it into PTB’s queue for processing
    application.update_queue.put(update)
    return "OK"

if __name__ == "__main__":
    # set your webhook exactly once on startup
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    application.bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000)
