import time
from telebot import TeleBot, types
from threading import Thread

# Initialize the bot
BOT_TOKEN = "7560808732:AAGhVR8Ik8of2rDOhVjxqonE5dNLPGSmVv4"
bot = TeleBot(BOT_TOKEN)

# Define the list of keywords
keywords = ["keyword1", "keyword2", "keyword3"]  # Replace with your keywords

# To handle reminders in parallel
def send_reminder(chat_id, keyword):
    time.sleep(60)  # Wait for 1 minute
    bot.send_message(chat_id, f"Reminder: {keyword}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message contains any keywords
    detected_keywords = [kw for kw in keywords if kw in message.text.lower()]

    if detected_keywords:
        # Reply to the user
        bot.reply_to(message, "I will update you in one minute!")
        
        # Send a reminder after 1 minute
        keyword_to_remind = detected_keywords[0]  # Take the first matching keyword
        Thread(target=send_reminder, args=(message.chat.id, keyword_to_remind)).start()

# Start the bot
print("Bot is running...")
bot.polling()