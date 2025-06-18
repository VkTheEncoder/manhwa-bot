import os
from flask import Flask, request
from telegram import Update
from bot import application    # your PTB Application instance

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

if __name__ == "__main__":
    application.run_polling()
