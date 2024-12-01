import time
from telebot import TeleBot
from threading import Thread
from queue import PriorityQueue
from datetime import datetime, timedelta

# Initialize the bot
BOT_TOKEN = "7787695982:AAEIs-cge0gW6fu4o9vdO02MyTkMHuQjgPc"
bot = TeleBot(BOT_TOKEN)

# Define constants
REMINDER_DELAY = 60*30  # Delay time in seconds (30 minutes )

# Define the list of keywords
keywords = [
    "отпиши", "обработай", "пройдись", "Отошел", "отошел", "Отошёл", "отошёл", "otoshel", "перерыв",
    "отошла", "ушла", "ушёл", "moved away", "пройдитесь", "отойду", "поменяй аву", "задача",
    "поменять переводчика", "включите все анкеты", "включите сендер", "пройдитесь по операм",
    "обработай олчат", "собрание", "поменять инвайты"
]

# Priority queue to manage reminders (sorted by datetime)
reminder_queue = PriorityQueue()

def reminder_worker():
    """Worker thread to process the reminder queue."""
    while True:
        if not reminder_queue.empty():
            # Get the next reminder
            scheduled_time, chat_id, keyword = reminder_queue.queue[0]  # Peek at the first item

            # Check if it's time to send the reminder
            if datetime.now() >= scheduled_time:
                reminder_queue.get()  # Remove the item from the queue
                bot.send_message(chat_id, f"напоминание: {keyword}")
            else:
                # Sleep until the nearest reminder's scheduled time
                time_to_wait = (scheduled_time - datetime.now()).total_seconds()
                time.sleep(min(time_to_wait, 1))  # Check frequently (every second)
        else:
            time.sleep(1)  # No reminders in the queue, wait and check again

# Start the worker thread
Thread(target=reminder_worker, daemon=True).start()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message contains any keywords
    detected_keywords = [kw for kw in keywords if kw in message.text.lower()]

    if detected_keywords:
        # Respond to the user immediately
        bot.reply_to(message, "Напомню через 30 минут!")

        # Add each keyword to the queue with a scheduled datetime
        for keyword in detected_keywords:
            reminder_time = datetime.now() + timedelta(seconds=REMINDER_DELAY)
            reminder_queue.put((reminder_time, message.chat.id, keyword))

# Start polling to keep the bot running
while True:
    try:
        bot.polling(timeout=86400, allowed_updates=None)  # Set high timeout and auto-reconnect
    except Exception as e:
        print(f"Bot crashed due to {e}. Restarting in 5 seconds...")
        time.sleep(5)  # Brief pause before restarting
