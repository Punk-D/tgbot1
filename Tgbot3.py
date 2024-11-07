import telebot

# Your bot token (from BotFather)
TOKEN = 'YOUR_BOT_TOKEN'

# Create a TeleBot instance using your token
bot = telebot.TeleBot(TOKEN)

# First message with keywords to trigger clues
first_clue_trigger = 'influenceproject'
second_clue_trigger = 'key'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the Syncra bot! Message me the clues you discover to progress in your journey.")

# Define a handler for messages
@bot.message_handler(func=lambda message: True)
def clue_handler(message):
    if message.text.lower() == first_clue_trigger:
        bot.send_message(
            message.chat.id,
            "You've discovered the first hint! Think about encryption and secure communications:\n\n"
            "- **Email**\n"
            "- **Encryption**\n"
            "- **CBC 128**\n\n"
            "Try to decipher the connection."
        )
    elif message.text.lower() == second_clue_trigger:
        bot.send_message(
            message.chat.id,
            "You're on the right path. The key you're looking for might be hidden in plain sight. Stay sharp!"
        )
    else:
        bot.send_message(message.chat.id, "I don't understand that. Try using the clues you've found so far!")

# Start the bot and keep it running
bot.polling()