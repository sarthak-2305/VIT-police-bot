from telegram import Update
from telegram.ext import ContextTypes

# Dictionary to keep track of warnings
warnings = {}

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the list of administrators and the group owner in the chat
    admins_and_owner = [
        admin.user.id for admin in await update.effective_chat.get_administrators()
        if admin.status in ["administrator", "creator"]
    ]

    # Check if the user issuing the command is an admin or the owner
    if update.effective_user.id in admins_and_owner:
        # Ensure a user is tagged with /warn command
        if context.args:
            username = context.args[0]
            
            # Increment warning count for the user
            if username in warnings:
                warnings[username] += 1
            else:
                warnings[username] = 1
            
            warning_count = warnings[username]
            
            # Send warning message to the user and the group
            warning_message = (
                f"⚠️ *Warning to {username}!* ⚠️\n"
                f"This is warning number {warning_count}. Kindly heed the rules of the realm, "
                "lest ye face sterner measures!"
            )
            await update.message.reply_text(warning_message, parse_mode='Markdown')
            
            # Optional: Take further action if warnings exceed a threshold
            if warning_count >= 3:
                further_action_message = (
                    f"{username} hath received {warning_count} warnings. "
                    "The admin may now consider silencing or removing the offender!"
                )
                await update.message.reply_text(further_action_message)
        else:
            await update.message.reply_text("Please mention a username to warn (e.g., /warn @username).")
    else:
        await update.message.reply_text("Only admins or the group owner can issue warnings.")
