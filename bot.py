import os
import time
from collections import defaultdict
from threading import Thread
from flask import Flask
import telebot

# 🌐 1. Mini Web Server to satisfy Render's port check
app = Flask('')


@app.route('/')
def home():
  return 'Bot is alive!'


def run_flask():
  # Grab Render's required port (defaults to 10000 if not set)
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


# 🏁 2. Bot Configuration (Safely fetched from Render Environment Variables)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 🛡️ Anti-Spam Tracker: Stores timestamps for each user
user_message_times = defaultdict(list)


# 🚨 3. Anti-Spam Check (13 messages under 6 seconds)
@bot.message_handler(
    func=lambda message: True, content_types=['text', 'photo', 'sticker', 'doc']
)
def anti_spam_check(message):
  # Ignore channel posts or system updates
  if not message.from_user:
    return

  user_id = message.from_user.id
  chat_id = message.chat.id
  current_time = time.time()

  # Remove timestamps older than 6 seconds
  user_message_times[user_id] = [
      t for t in user_message_times[user_id] if current_time - t <= 6
  ]

  # Add current message timestamp
  user_message_times[user_id].append(current_time)

  # If user sends 13 or more messages in 6 seconds -> Mute them!
  if len(user_message_times[user_id]) >= 13:
    user_message_times[user_id] = []  # Reset count
    until_time = int(current_time) + 60  # Mute for 60 seconds (1 minute)

    try:
      bot.restrict_chat_member(
          chat_id, user_id, until_date=until_time, can_send_messages=False
      )
      bot.reply_to(
          message,
          '<b>muted for 1 minute</b>\n<b>reason:</b> spamming detected 🚫',
          parse_mode='HTML',
      )
    except Exception as e:
      print(f'Failed to mute user: {e}')


# 💬 4. Command Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_name = message.from_user.first_name
  welcome_text = (
      f'Hello {user_name}! Welcome to Minecraft Myanmar. Please join to our'
      " channel and group and let's discuss about minecraft ! Channel ="
      ' https://t.me/minecraftmyanmar_addrons      Group ='
      ' https://t.me/minecraftmyanmar_chat'
  )
  bot.reply_to(message, welcome_text)


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
  for new_member in message.new_chat_members:
    if new_member.id != bot.get_me().id:
      group_welcome = (
          f"Welcome to the group, {new_member.first_name}! Let's discuss about"
          ' minecraft!'
      )
      bot.send_message(message.chat.id, group_welcome)


# 🚀 Start Flask in a background thread FIRST, then start Telegram bot
if __name__ == '__main__':
  # Start Web Server in background thread
  flask_thread = Thread(target=run_flask)
  flask_thread.daemon = True
  flask_thread.start()

  print('Bot is racing and ready to go! 🏁')
  # Start Telegram Bot polling
  bot.infinity_polling()
