import os
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


# 🏁 2. Bot Configuration
BOT_TOKEN = '8961144422:AAEbEX-xxgi3hhXnHRVCT5g7o5oQPpEaafY'
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_name = message.from_user.first_name
  welcome_text = (
      f'Hello {user_name}! Welcome to Minecraft Myanmar. Please join to our'
      ' channel and group and let\'s discuss about minecraft ! Channel ='
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
