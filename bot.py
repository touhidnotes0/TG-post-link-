from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def build_post_link(update: Update) -> str | None:
    chat = update.effective_chat
    msg = update.effective_message
    if not chat or not msg:
        return None

    # Public group/channel must have username
    if chat.username:
        return f"https://t.me/{chat.username}/{msg.message_id}"

    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Post Link Bot ready!\n\n"
        "✅ Add me to a PUBLIC group (with @username).\n"
        "When anyone sends a photo or text, I reply with:\n"
        "• Open original post link\n\n"
        "⚠️ If the group is private (no username), Telegram doesn't allow public post links."
    )


async def handle_any(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = build_post_link(update)

    if link:
        await update.message.reply_text(f"🔗 Open original post:\n{link}")
    else:
        await update.message.reply_text(
            "ℹ️ I can generate 'Open original post' links only in PUBLIC groups.\n"
            "Make your group public and set a username (t.me/yourgroupname)."
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

# Respond to photos, videos, documents, and normal text (excluding commands)
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, handle_any))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any))

app.run_polling()
