import os
import threading
from flask import Flask
import telebot

# 1. Initialize Telegram Bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. Initialize Flask Web Server
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot is alive!', 200


def run_flask():
  app.run(host='0.0.0.0', port=10000)


# 3. Command Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
  welcome_text = 'Hey Hudson! 👋 I am online, active, and ready to go! 🏁🔥'
  bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, 'Send me any message or command!')


# 4. Main Execution
if __name__ == '__main__':
  # Start Flask background thread
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.daemon = True
  flask_thread.start()

  print('Bot is racing and ready to go! 🏁')

  # Start polling without the broken keyword
  bot.infinity_polling(skip_pending=True)
