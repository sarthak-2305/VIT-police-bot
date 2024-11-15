from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from datetime import timedelta
from utils.permissions import is_admin_or_owner

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ensure the command issuer is an admin or the owner
    if await is_admin_or_owner(update):
        if len(context.args) >= 2:
            username = context.args[0]
            try:
                mute_duration = int(context.args[1])
            except ValueError:
                await update.message.reply_text("Please provide a valid number for the mute duration (in minutes).")
                return
            
            # Attempt to get user by username
            try:
                user_to_mute = await update.effective_chat.get_member(username.replace('@', ''))
            except:
                await update.message.reply_text("User not found. Ensure they are in the group and the username is correct.")
                return

            # Proceed to mute if user is found
            if user_to_mute:
                mute_until = timedelta(minutes=mute_duration)
                await context.bot.restrict_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=user_to_mute.user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=mute_until
                )
                await update.message.reply_text(
                    f"{username} has been muted for {mute_duration} minutes. 🛑"
                )
            else:
                await update.message.reply_text("Could not locate the specified user in the group.")
        else:
            await update.message.reply_text("Usage: /mute @username <time_in_minutes>")
    else:
        await update.message.reply_text("Only admins or the group owner can mute members.")
