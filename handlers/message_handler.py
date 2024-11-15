from predictor import get_model_predictions, aggregate_predictions
from telegram import Update
from telegram.ext import ContextTypes
import datetime

def log_hate_speech(message_content, user_info):
    # Define the log entry format
    log_entry = f"Timestamp: {datetime.datetime.now()}\nUser: {user_info}\nMessage: {message_content}\n{'-'*40}\n"
    
    # Append the entry to the log file
    with open("hate_speech_log.txt", "a") as log_file:
        log_file.write(log_entry)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Get predictions from each model
    model_predictions = get_model_predictions(text)
    
    # Aggregate predictions using voting
    final_label, vote_summary = aggregate_predictions(model_predictions)
    
    # Take action based on aggregated result
    if final_label == 1:
        # Delete the message if classified as hate speech
        await update.message.delete()
        
        # Log the hate speech message
        user_info = f"{update.effective_user.username or update.effective_user.id}"
        log_hate_speech(text, user_info)

        # Optional: Send a warning to the user after deletion
        response = f"⚠️ A message was removed as it violated our community standards. We strive to ensure a respectful and welcoming environment for all members."
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    # else:
    #     response = "this message is safe"
    #     await update.message.reply_text(response)
