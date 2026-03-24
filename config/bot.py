import os
import django

# Django settings bilan bog'lash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async
from users.models import TelegramUser

TOKEN = "8607364026:AAFTo-eVjidDbdhL7Bj6E3mz_lsfP_xmyRk"

# ORM chaqiruvi async uchun wrapper
@sync_to_async
def create_or_get_user(telegram_id, username, first_name, last_name):
    obj, created = TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    return obj

# Async start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    telegram_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    # 1. DATABASE GA YOZISH / Olish
    db_user = await create_or_get_user(telegram_id, username, first_name, last_name)

    # 2. USERGA YUBORISH
    text = f"""
✅ Siz ro'yxatdan o'tdingiz!

ID: {db_user.telegram_id}
Username: {db_user.username}
Name: {db_user.first_name} {db_user.last_name}
"""
    await update.message.reply_text(text)

# Bot yaratish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot ishga tushdi...")
app.run_polling()

