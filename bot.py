import os
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.extractor import pdf_to_images
from utils.ocr import ocr_image
from utils.openai_client import summarize_text

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
bot = app.bot
dp = app.dispatcher

@dp.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text('Send me a PDF of your manhwa!')))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # handled by decorator

@dp.add_handler(MessageHandler(filters.Document.FileExtension('pdf'), lambda u, c: handle_pdf(u, c)))
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    pdf = await update.message.document.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, 'input.pdf')
        await pdf.download_to_drive(pdf_path)
        images = pdf_to_images(pdf_path, tmpdir)
        output_txt = os.path.join(tmpdir, 'summary.txt')
        with open(output_txt, 'w', encoding='utf-8') as out:
            for img_path in images:
                text = ocr_image(img_path)
                summary = summarize_text(text)
                out.write(summary + '\n\n')
        await context.bot.send_document(chat_id=user_id, document=output_txt)
