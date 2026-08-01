import os
import threading
from flask import Flask
import telebot

# 1. Initialize Telegram Bot using Environment Variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. Initialize Flask Web Server (keeps Render awake!)
app = Flask(__name__)


@app.route('/')
def home():
  return 'Bot is alive!', 200


def run_flask():
  app.run(host='0.0.0.0', port=10000)


# 3. /start Command Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
  welcome_text = (
      'Hey Hudson! 👋 I am online, active, and ready to race! 🏁🔥\n\nSend me'
      ' a command or message to get started!'
  )
  bot.reply_to(message, welcome_text)


# 4. /help Command Handler (Optional extra command)
@bot.message_handler(commands=['help'])
def send_help(message):
  help_text = (
      'Here are my available commands:\n/start - Start the bot\n/help - Get'
      ' help info'
  )
  bot.reply_to(message, help_text)


# 5. Main Execution Block
if __name__ == '__main__':
  # Start Flask in a background thread
  flask_thread = threading.Thread(target=run_flask)
  flask_thread.daemon = True
  flask_thread.start()

  print('Bot is racing and ready to go! 🏁')

  # Start listening for Telegram updates (skips old missed messages on startup)
  bot.infinity_polling(skip_pending_sessions=True)
