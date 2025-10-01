from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import logging

# Logging setup (optional but recommended)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Bot token from Render environment variable
TOKEN = os.getenv("BOT_TOKEN")  # Never hardcode token
ADMIN_ID = 1924265817           # Your numeric Telegram ID
bot_active = True

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot chal raha hai!")

# /toggle command (only admin can toggle ON/OFF)
async def toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_active
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        bot_active = not bot_active
        status = "ON" if bot_active else "OFF"
        await update.message.reply_text(f"✅ Bot {status} ho gaya.")
    else:
        await update.message.reply_text("❌ Aapko permission nahi hai.")

# Auto-reply for messages
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_active:
        return
    if update.message and update.message.text:
        text = update.message.text.lower()
        if "create" in text:
            await update.message.reply_text("I do")
        elif "bye" in text:
            await update.message.reply_text("Goodbye 👋")
        elif "hello" in text:
            await update.message.reply_text("Hi 👋")

if __name__ == "__main__":
    print("Starting bot...")

    # Create the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("toggle", toggle))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot is running...")
    app.run_polling()
