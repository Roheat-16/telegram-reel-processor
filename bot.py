import os
import yt_dlp
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WATERMARK = "watermark.png"

def download_reel(url):
    ydl_opts = {
        'outtmpl': 'input.%(ext)s',
        'format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "input.mp4"

def add_watermark(input_video):
    output = "output.mp4"

    command = [
        "ffmpeg",
        "-i", input_video,
        "-i", WATERMARK,
        "-filter_complex", "overlay=W-w-10:H-h-10",
        "-codec:a", "copy",
        output
    ]

    subprocess.run(command)
    return output

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ Processing your reel...")

    try:
        video = download_reel(url)
        final_video = add_watermark(video)

        await update.message.reply_video(video=open(final_video, 'rb'))

        os.remove(video)
        os.remove(final_video)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

if __name__ == "__main__":
    print("🤖 Bot is running...")
    app.run_polling()
