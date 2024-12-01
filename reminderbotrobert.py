import time
from telebot import TeleBot
from threading import Thread
from queue import Queue

# Initialize the bot
BOT_TOKEN = "7787695982:AAEIs-cge0gW6fu4o9vdO02MyTkMHuQjgPc"
bot = TeleBot(BOT_TOKEN)

# Define constants
REMINDER_DELAY = 120  # Set reminder time in seconds (2 minutes for testing)

# Define the list of keywords
keywords = [
    "отпиши", "обработай", "пройдись", "Отошел", "отошел", "Отошёл", "отошёл", "otoshel", "перерыв",
    "отошла", "ушла", "ушёл", "moved away", "пройдитесь", "отойду", "поменяй аву", "задача",
    "поменять переводчика", "включите все анкеты", "включите сендер", "пройдитесь по операм",
    "обработай олчат", "собрание", "поменять инвайты"
]

# Queue to store reminders
reminder_queue = Queue()

# Threaded worker to process reminders
def reminder_worker():
    while True:
        chat_id, keyword = reminder_queue.get()  # Retrieve the next reminder
        time.sleep(REMINDER_DELAY)  # Wait for the defined reminder delay
        bot.send_message(chat_id, f"напоминание: {keyword}")
        reminder_queue.task_done()  # Mark the reminder as processed

# Start the reminder worker thread
Thread(target=reminder_worker, daemon=True).start()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    # Check if the message contains any keywords
    detected_keywords = [kw for kw in keywords if kw in message.text.lower()]

    if detected_keywords:
        # Reply to the user immediately
        bot.reply_to(message, "Напомню через 2 минуты!")
        
        # Queue reminders for all detected keywords
        for keyword in detected_keywords:
            reminder_queue.put((chat_id, keyword))  # Add the reminder to the queue

# Start polling to keep the bot running
while True:
    try:
        bot.polling(timeout=86400, allowed_updates=None)  # Set high timeout and auto-reconnect
    except Exception as e:
        print(f"Bot crashed due to {e}. Restarting in 5 seconds...")
        time.sleep(5)  # Brief pause before restarting
