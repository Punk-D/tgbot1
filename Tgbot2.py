import telebot

# Your bot token (from BotFather)
TOKEN = '8158170604:AAHzUDShobxPIDwB-9xRFTyIkuAF8K4-NpQ'

# Create a TeleBot instance using your token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bot1")

# Define a handler for messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'B':  # Check if the message is "B"
        bot.send_message(message.chat.id, """import telebot

# Your bot token (from BotFather)
TOKEN = '8158170604:AAHzUDShobxPIDwB-9xRFTyIkuAF8K4-NpQ'

# Create a TeleBot instance using your token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bot1")

# Define a handler for messages
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text == 'B':  # Check if the message is "B"
        bot.send_message(message.chat.id, 'A')  # Respond with "A"
    elif message.text == "Reply B":
        bot.reply_to(message, 'A')

# Start the bot and keep it running
bot.polling()
""")  # Respond with "A"
    elif message.text == "Reply B":
        bot.reply_to(message, 'A')

# Start the bot and keep it running
bot.polling()
