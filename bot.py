import os
import tempfile
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from utils.extractor import pdf_to_images
from utils.ocr import ocr_image
from utils.openai_client import summarize_image_panel

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
PORT = int(os.environ.get("PORT", 10000))

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a PDF of your manhwa!")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    pdf_file = await update.message.document.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "input.pdf")
        await pdf_file.download_to_drive(pdf_path)

        images = pdf_to_images(pdf_path, tmpdir)
        output_txt = os.path.join(tmpdir, "summary.txt")
        with open(output_txt, "w", encoding="utf-8") as out:
            for img in images:
                text = ocr_image(img)
                summary = summarize_image_panel(text)
                out.write(summary + "\n\n")

        await context.bot.send_document(chat_id=user_id, document=output_txt)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(MessageHandler(filters.Document.FileExtension("pdf"), handle_pdf))

    # This method will:
    # 1) set the webhook to WEBHOOK_URL + "/webhook"
    # 2) start a webserver on 0.0.0.0:PORT
    # 3) begin dispatching incoming updates via that webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
    )

if __name__ == "__main__":
    main()
