import telebot

# Your bot token
BOT_TOKEN = '8961144422:AAEbEX-xxgi3hhXnHRVCT5g7o5oQPpEaafY'

bot = telebot.TeleBot(BOT_TOKEN)

# 🏁 1. Private Message /start Trigger
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name 
    welcome_text = f"Hello {user_name}! Welcome to Minecraft Myanmar. Please join to our channel and group and let's discuss about minecraft ! Channel = https://t.me/minecraftmyanmar_addrons      Group = https://t.me/minecraftmyanmar_chat"
    bot.reply_to(message, welcome_text)

# 👥 2. Group Join Greeting
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.id != bot.get_me().id:
            group_welcome = f"Welcome to the group, {new_member.first_name}! Let's discuss about minecraft!"
            bot.send_message(message.chat.id, group_welcome)

print("Bot is racing and ready to go! 🏁")
bot.infinity_polling()
