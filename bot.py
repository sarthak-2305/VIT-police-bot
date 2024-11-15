import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from handlers.start_handler import start
from handlers.warn_handler import warn
from handlers.mute_handler import mute
from handlers.message_handler import handle_message

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot
app = Application.builder().token(BOT_TOKEN).build()

# Register command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("mute", mute))
# Register the message handler to capture all text messages
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    app.run_polling()
