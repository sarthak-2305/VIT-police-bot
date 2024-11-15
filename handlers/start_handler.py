from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_message = (
        "Hello! Welcome to our community. This bot is here to help maintain a respectful and inclusive environment for everyone. Please adhere to the group guidelines."
    )
    await update.message.reply_text(intro_message, parse_mode='Markdown')
