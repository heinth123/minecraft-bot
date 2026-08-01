import os
import time
import threading
from collections import defaultdict
from flask import Flask
import telebot
from telebot import types

# ---------------------------------------------------------
# 1. FLASK KEEP-ALIVE SERVER (For Render Web Service)
# ---------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------------------------------------------------------
# 2. TELEGRAM BOT INITIALIZATION
# ---------------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Anti-spam tracking settings (13 messages in 6 seconds)
user_messages = defaultdict(list)
SPAM_THRESHOLD = 13
TIME_WINDOW = 6
MUTE_DURATION = 60

# ---------------------------------------------------------
# 3. COMMAND HANDLERS
# ---------------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Hello {user_name}! Welcome to Minecraft Myanmar. "
        f"Please join to our channel and group and let's discuss about minecraft !\n"
        f"Channel = https://t.me/minecraftmyanmar_addrons\n"
        f"Group = https://t.me/minecraftmyanmar_chat"
    )
    bot.reply_to(message, welcome_text)

# ---------------------------------------------------------
# 4. ANTI-SPAM HANDLER (Group Chats)
# ---------------------------------------------------------
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'sticker', 'document'])
def anti_spam_handler(message):
    # Only run in group/supergroup
    if message.chat.type not in ['group', 'supergroup']:
        return

    # Skip admins so they don't get muted
    try:
        member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if member.status in ['administrator', 'creator']:
            return
    except Exception:
        pass

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    # Clean old timestamps
    user_messages[user_id] = [t for t in user_messages[user_id] if current_time - t < TIME_WINDOW]
    user_messages[user_id].append(current_time)

    # Check if threshold hit
    if len(user_messages[user_id]) > SPAM_THRESHOLD:
        try:
            # Delete spam message
            bot.delete_message(chat_id, message.message_id)

            # Mute user for 1 minute
            until_time = int(current_time + MUTE_DURATION)
            bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                ),
                until_date=until_time
            )

            # Send your exact warning message
            username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
            bot.send_message(
                chat_id, 
                f"{username} was muted for 1 minute, reason: spam detected"
            )

            user_messages[user_id].clear()
        except Exception as e:
            print(f"Anti-spam error: {e}")

# ---------------------------------------------------------
# 5. MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Bot is racing and ready to go! 🏁")
    
    # Start Flask server in background thread
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Start bot polling
    bot.infinity_polling()
