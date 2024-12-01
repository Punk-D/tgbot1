import time
from telebot import TeleBot, types
from threading import Thread

# Initialize the bot
BOT_TOKEN = "7787695982:AAEIs-cge0gW6fu4o9vdO02MyTkMHuQjgPc"
bot = TeleBot(BOT_TOKEN)

# Define the list of keywords
keywords = [
    "отпиши", "обработай", "пройдись", "Отошел", "отошел", "Отошёл", "отошёл", "otoshel", "перерыв",
    "отошла", "ушла", "ушёл", "moved away", "пройдитесь", "отойду", "поменяй аву", "задача",
    "поменять переводчика", "включите все анкеты", "включите сендер", "пройдитесь по операм",
    "обработай олчат", "собрание", "поменять инвайты"
]

# To handle reminders in parallel
def send_reminder(chat_id, keyword):
    time.sleep(1800)  # Wait for 30 minutes
    bot.send_message(chat_id, f"напоминание: {keyword}")

# Set to store chat IDs that have already triggered a reminder
handled_chats = set()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in handled_chats:
        return  # Ignore subsequent messages from this user

    # Check if the entire message matches a keyword exactly
    message_text = message.text.strip().lower()  # Normalize input
    detected_keywords = [kw for kw in keywords if kw.lower() == message_text]

    if detected_keywords:
        # Reply to the user
        bot.reply_to(message, "Напомню через 30 минут!")

        # Send a reminder after 30 minutes
        keyword_to_remind = detected_keywords[0]  # Take the first matching keyword
        handled_chats.add(chat_id)  # Mark this user as handled
        Thread(target=send_reminder, args=(chat_id, keyword_to_remind)).start()

# Start polling to keep the bot running
while True:
    try:
        bot.polling(timeout=86400, allowed_updates=None)  # Set high timeout and auto-reconnect
    except Exception as e:
        print(f"Bot crashed due to {e}. Restarting in 5 seconds...")
        time.sleep(5)  # Brief pause before restarting