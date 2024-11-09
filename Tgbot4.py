import telebot
import subprocess
import os
import sys
import json
import random
import time

# Bot token and authorized user ID for updates
TOKEN = '7584853291:AAEspOE5KMS9_eFbX3vYDWDBnomENo8yAbM'
AUTHORIZED_USER_ID = 765139248  # Replace with your Telegram user ID for updates

CHATLOGTOKEN = '7239305488:AAG7CVDzdbpU_ac1oskQVBGijlQMukUay2o'

# Contract number and predefined responses in Freeman Mode
CONTRACT_NUMBER = '413'
FREEMAN_MODE_FILE = 'freeman_mode_users.json'  # JSON file to store user progress

# Predefined Freeman Mode responses
responses = {
    "diary": "Oh, you want to see my diary? I bet you already know where it is. The key to decrypt those files is: influenceproject",
    "code": "The company hides more than it shows. Watch out for subtle messages."
}
hints = [
    "Be attentive. Start with CBC 128 encryption.",
    "Remember, the files are encrypted for a reason.",
    "Subtle details matter. Trust your instincts.",
    "The key is hidden, but it’s not far away.",
]

# Load Freeman Mode data from file
def load_freeman_mode_data():
    if os.path.exists(FREEMAN_MODE_FILE):
        with open(FREEMAN_MODE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save Freeman Mode data to file
def save_freeman_mode_data(data):
    with open(FREEMAN_MODE_FILE, 'w') as file:
        json.dump(data, file)

# Initialize bot and load data
bot = telebot.TeleBot(TOKEN)
users_in_freeman_mode = load_freeman_mode_data()

chatlogbot = telebot.TeleBot(CHATLOGTOKEN)

# Cooldown duration in seconds (4 hours = 14400 seconds)
HINT_COOLDOWN = 14400  # 4 hours

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to SyncraHelperBot. I’m here to assist you with basic calculations. Send me a math problem!")

@bot.message_handler(commands=['update'])
def update_bot(message):
    # Only allow the authorized user to run updates
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Checking for updates...")
        try:
            subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
            bot.send_message(message.chat.id, "Bot updated successfully.")
            # Restart the bot
            os.execv(sys.executable, ['python'] + sys.argv)
        except subprocess.CalledProcessError:
            bot.send_message(message.chat.id, "Failed to update the bot. Please check the repository.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to update the bot.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    chatlogbot.send_message(AUTHORIZED_USER_ID, message.from_user.username+" : "+message.text)
    
    # Check if the user is in Freeman Mode
    if user_id in users_in_freeman_mode:
        # Handle "Freeman Mode" responses
        if message.text in responses and message.text not in users_in_freeman_mode[user_id]:
            bot.send_message(message.chat.id, responses[message.text])
            users_in_freeman_mode[user_id].append(message.text)  # Mark response as used
            save_freeman_mode_data(users_in_freeman_mode)  # Save the updated data
        elif message.text in users_in_freeman_mode[user_id]:
            bot.send_message(message.chat.id, "We’ve already covered that.")
        elif message.text == "hint":
        # Handle cooldown for hints
        current_time = time.time()
        last_hint_time = users_in_freeman_mode[user_id].get("last_hint_time", 0)

            # Check if the user is within the cooldown period
            if current_time - last_hint_time < HINT_COOLDOWN:
                remaining_time = int(HINT_COOLDOWN - (current_time - last_hint_time))
                hours, remainder = divmod(remaining_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                bot.send_message(message.chat.id, f"You must wait {hours} hours, {minutes} minutes before asking for another hint.")
            else:
                # Check if there are unused hints
                unused_hints = [hint for hint in responses["hint"] if hint not in users_in_freeman_mode[user_id]["hints_given"]]

            if unused_hints:
                # Provide a random unused hint
                hint = random.choice(unused_hints)
                bot.send_message(message.chat.id, hint)
                # Track the provided hint
                users_in_freeman_mode[user_id]["hints_given"].append(hint)
                users_in_freeman_mode[user_id]["last_hint_time"] = current_time  # Update last hint time
                save_freeman_mode_data(users_in_freeman_mode)  # Save the updated data
            else:
                bot.send_message(message.chat.id, "You’ve already received all the hints. Time to solve this puzzle on your own!")
        else:
            bot.send_message(message.chat.id, "I’m afraid I don’t have information on that topic.")
    
    elif message.text == CONTRACT_NUMBER:
        # Activate Freeman Mode for this specific user
        users_in_freeman_mode[user_id] = {"hints_given": []}  # Initialize data with an empty list for tracking used hints
        save_freeman_mode_data(users_in_freeman_mode)
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}. I see your curiosity led you far. I can answer if you’re on the right path.")
    
    

    elif message.text.replace(" ", "").isdigit():
        # Calculator Mode
        try:
            result = eval(message.text)
            bot.send_message(message.chat.id, f"The answer is: {result}")
        except Exception:
            bot.send_message(message.chat.id, "I can’t process that. Please enter a valid arithmetic expression.")
    
    else:
        # Default response for unrecognized messages outside of Freeman Mode
        bot.send_message(message.chat.id, "I don't know who you are and what you want. If you won't type your number, I'll ignore you. Updated")

# Start polling to keep the bot running
bot.polling()
