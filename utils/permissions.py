from telegram import Update

async def is_admin_or_owner(update: Update):
    admins_and_owner = [
        admin.user.id for admin in await update.effective_chat.get_administrators()
        if admin.status in ["administrator", "creator"]
    ]
    return update.effective_user.id in admins_and_owner
