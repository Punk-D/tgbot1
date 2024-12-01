import time
from telebot import TeleBot, types
from threading import Thread

# Initialize the bot
BOT_TOKEN = "7787695982:AAEIs-cge0gW6fu4o9vdO02MyTkMHuQjgPc"
bot = TeleBot(BOT_TOKEN)

# Define the list of keywords
keywords = ["отпиши", "обработай", "пройдись", "Отошел", "отошел", "Отошёл", "отошёл", "otoshel", "перерыв",
    "отошла", "ушла", "ушёл", "moved away", "пройдитесь", "отойду", "поменяй аву", "задача",
    "поменять переводчика", "включите все анкеты", "включите сендер", "пройдитесь по операм",
    "обработай олчат", "собрание", "поменять инвайты"]  # Replace with your keywords


# To handle reminders in parallel
def send_reminder(chat_id, keyword):
    time.sleep(1800)  # Wait for 1 minute
    bot.send_message(chat_id, f"напоминание: {keyword}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Check if the message contains any keywords
    detected_keywords = [kw for kw in keywords if kw in message.text.lower()]

    if detected_keywords:
        # Reply to the user
        bot.reply_to(message, "Напомню через 30 минут!")

        # Send a reminder after 1 minute
        keyword_to_remind = detected_keywords[0]  # Take the first matching keyword
        Thread(target=send_reminder, args=(message.chat.id, keyword_to_remind)).start()


# Start the bot
print("Bot is running...")
bot.polling()