import telebot
from datetime import datetime, timedelta
import threading
import time

# Replace 'YOUR_BOT_TOKEN' with the bot token you got from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

# List to store user IDs of those who sent /start
user_ids = set()

# Function to calculate days until New Year
def days_till_new_year():
    today = datetime.now()
    new_year = datetime(today.year + 1, 1, 1)
    return (new_year - today).days

# Function to send the message to all users
def send_new_year_message():
    message = f"Days till New Year: {days_till_new_year()}"
    for user_id in user_ids:
        try:
            bot.send_message(user_id, message)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

# Background task to send the message every 24 hours
def schedule_daily_message():
    while True:
        send_new_year_message()
        time.sleep(86400)  # Wait 24 hours

# Start the background thread
threading.Thread(target=schedule_daily_message, daemon=True).start()

# Handle /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_ids.add(message.chat.id)
    bot.reply_to(message, "Welcome! You'll now receive daily updates about the days left until New Year.")

# Handle any text message
@bot.message_handler(func=lambda m: True)
def respond_to_message(message):
    user_ids.add(message.chat.id)  # Add user to the list if not already added
    bot.reply_to(message, f"Days till New Year: {days_till_new_year()}")

# Start polling
while True:
    try:
        bot.polling(timeout=86400, allowed_updates=None)  # Set high timeout and auto-reconnect
    except Exception as e:
        print(f"Bot crashed due to {e}. Restarting in 5 seconds...")
        time.sleep(5)  # Brief pause before restarting
