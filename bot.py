from telegram.ext import Updater, MessageHandler, Filters
import requests
import os

print("🤖 Bot is starting...")

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
SCRIPT_URL = os.environ['SCRIPT_URL']

# Store user IDs mapped to sheet names
user_map = {
    27499437: "Sush",   # Replace with actual Sush user ID
    21694601: "Soum"    # Replace with actual Soum user ID
}

def handle_message(update, context):
    user_id = update.message.from_user.id
    chat = update.message.chat
    text = update.message.text.strip()

    if user_id not in user_map:
        update.message.reply_text("You are not authorized to use this bot.")
        return

    try:
        amount_str, item = text.split(' ', 1)
        amount = float(amount_str)

        payload = {
            'user_id': user_id,
            'amount': amount,
            'item': item
        }

        response = requests.post(SCRIPT_URL, json=payload)

        if response.status_code == 200:
            update.message.reply_text(f"Logged: ${amount} on {item}")
        else:
            update.message.reply_text("Failed to log expense.")

    except:
        update.message.reply_text("Invalid format. Use: '10 lunch'")

updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()
