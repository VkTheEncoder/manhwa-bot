import os
from flask import Flask, request
from bot import dp, bot

app = Flask(__name__)

@app.route('/healthz')
def health():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json(force=True)
    dp.process_update(update)
    return 'OK'

if __name__ == '__main__':
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    WEBHOOK_URL = os.environ['WEBHOOK_URL']
    bot.set_webhook(WEBHOOK_URL)
    app.run(host='0.0.0.0', port=5000)
