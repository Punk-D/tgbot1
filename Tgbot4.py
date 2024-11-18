import telebot
import subprocess
import os
import sys
import json
import time

# Bot token and authorized user ID for updates
TOKEN = '7584853291:AAEspOE5KMS9_eFbX3vYDWDBnomENo8yAbM'
AUTHORIZED_USER_ID = 765139248  # Replace with your Telegram user ID for updates

CHATLOGTOKEN = '7239305488:AAG7CVDzdbpU_ac1oskQVBGijlQMukUay2o'

# Contract number and predefined responses in Freeman Mode
CONTRACT_NUMBER = '413'
FREEMAN_MODE_FILE = 'freeman_mode_users.json'  # JSON file to store user progress
HINTS_FILE = 'hints_data.json'  # JSON file to store hints and responses

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

# Load hints data from JSON file (or create it if it doesn't exist)
def load_hints_data():
    if os.path.exists(HINTS_FILE):
        with open(HINTS_FILE, 'r') as file:
            return json.load(file)
    return {"simple_hints": [], "keyword_responses": {}}

# Save hints data to JSON file
def save_hints_data(data):
    with open(HINTS_FILE, 'w') as file:
        json.dump(data, file)

# Initialize bot and load data
bot = telebot.TeleBot(TOKEN)
users_in_freeman_mode = load_freeman_mode_data()
hints_data = load_hints_data()

chatlogbot = telebot.TeleBot(CHATLOGTOKEN)

# Cooldown duration in seconds (2 hours = 7200 seconds)
HINT_COOLDOWN = 7200  # 2 hours

# Function to send log message to chatlogbot
def send_to_logbot(message_text):
    chatlogbot.send_message(AUTHORIZED_USER_ID, message_text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to SyncraHelperBot. I’m here to assist you with basic calculations. Send me a math problem!")

@bot.message_handler(commands=['help'])
def help_command(message):
    # Only allow the authorized user to access the help command
    if message.from_user.id == AUTHORIZED_USER_ID:
        help_text = (
            "Here’s a list of available commands you can use:\n\n"
            "/start - Start interacting with the bot.\n\n"
            "/update - Update the bot from the GitHub repository (only for authorized users).\n\n"
            "/add_hint <hint> - Add a simple hint to the list.\n"
            "/add_hint <hint> <response> - Add a keyword-response pair to the hints.\n\n"
            "/browse_hints - Browse all available hints with their IDs.\n\n"
            "/remove_hint hint<ID> - Remove a hint by its ID (e.g., 'hint1', 'hint2').\n\n"
            "Freeman Mode:\n"
            "   - When in Freeman Mode, you can interact with hints and responses based on the contract number.\n"
            "   - Type 'hint' to get a hint after the cooldown period.\n"
            "   - Type a keyword to get the corresponding response.\n\n"
            "Hint Cooldown: You can only request a hint once every 2 hours.\n\n"
            "Please use these commands responsibly and feel free to reach out if you need further assistance."
        )
        bot.send_message(message.chat.id, help_text)
        send_to_logbot(f"Bot to User: Help message sent.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to view help commands.")


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

@bot.message_handler(commands=['add_hint'])
def add_hint(message):
    # Only allow the authorized user to add hints
    if message.from_user.id == AUTHORIZED_USER_ID:
        # Expecting format: /add_hint <hint> <response> or /add_hint <hint>
        parts = message.text.split(' ', 2)  # Split only into 3 parts max
        if len(parts) == 3:
            # Adding a keyword-response pair
            hint = parts[1].strip()
            response = parts[2].strip()
            hints_data["keyword_responses"][hint] = response
            save_hints_data(hints_data)
            bot.send_message(message.chat.id, f"Keyword-Response pair added: '{hint}' -> '{response}'")
            send_to_logbot(f"Added new keyword-response: '{hint}' -> '{response}'")
        elif len(parts) == 2:
            # Adding a simple hint (with spaces in the hint itself)
            hint = parts[1].strip()
            hints_data["simple_hints"].append(hint)
            save_hints_data(hints_data)
            bot.send_message(message.chat.id, f"Simple hint added: '{hint}'")
            send_to_logbot(f"Added new simple hint: '{hint}'")
        else:
            bot.send_message(message.chat.id, "Invalid format. Use: /add_hint <hint> <response> or /add_hint <hint>")


@bot.message_handler(commands=['browse_hints'])
def browse_hints(message):
    # Only allow the authorized user to browse hints
    if message.from_user.id == AUTHORIZED_USER_ID:
        hint_list = []
        
        # Simple hints browsing
        for idx, hint in enumerate(hints_data["simple_hints"], start=1):
            hint_list.append(f"hint{idx}: {hint}")
        
        # Keyword response browsing
        for idx, (hint, response) in enumerate(hints_data["keyword_responses"].items(), start=len(hints_data["simple_hints"]) + 1):
            hint_list.append(f"hint{idx}: '{hint}' -> '{response}'")
        
        if hint_list:
            bot.send_message(message.chat.id, "\n".join(hint_list))
            send_to_logbot(f"Bot to User: Browsing hints: \n" + "\n".join(hint_list))
        else:
            bot.send_message(message.chat.id, "No hints available yet.")
            send_to_logbot(f"Bot to User: No hints available yet.")

@bot.message_handler(commands=['remove_hint'])
def remove_hint(message):
    # Only allow the authorized user to remove hints
    if message.from_user.id == AUTHORIZED_USER_ID:
        # Expecting format: /remove_hint hint<ID>
        parts = message.text.split(' ', 1)
        if len(parts) == 2:
            hint_id = parts[1].strip()
            try:
                # Determine which type of hint (simple or keyword) to remove
                if hint_id.startswith('hint'):
                    idx = int(hint_id[4:]) - 1  # Remove hint with index (hint1 -> 0, hint2 -> 1, etc.)
                    if idx < len(hints_data["simple_hints"]):
                        removed_hint = hints_data["simple_hints"].pop(idx)
                        save_hints_data(hints_data)
                        bot.send_message(message.chat.id, f"Removed simple hint: '{removed_hint}'")
                        send_to_logbot(f"Removed simple hint: '{removed_hint}'")
                    elif idx - len(hints_data["simple_hints"]) < len(hints_data["keyword_responses"]):
                        # Adjust index for keyword responses
                        keyword_idx = idx - len(hints_data["simple_hints"])
                        removed_keyword = list(hints_data["keyword_responses"].keys())[keyword_idx]
                        removed_response = hints_data["keyword_responses"].pop(removed_keyword)
                        save_hints_data(hints_data)
                        bot.send_message(message.chat.id, f"Removed keyword hint: '{removed_keyword}' -> '{removed_response}'")
                        send_to_logbot(f"Removed keyword hint: '{removed_keyword}' -> '{removed_response}'")
                    else:
                        bot.send_message(message.chat.id, f"Hint ID '{hint_id}' does not exist.")
                        send_to_logbot(f"Bot to User: Hint ID '{hint_id}' does not exist.")
                else:
                    bot.send_message(message.chat.id, "Invalid hint ID format. Use 'hint<ID>'.")
            except ValueError:
                bot.send_message(message.chat.id, "Invalid hint ID format. Use 'hint<ID>'.")
                send_to_logbot(f"Bot to User: Invalid hint ID format. Use 'hint<ID>'.")
        else:
            bot.send_message(message.chat.id, "Please provide a hint ID to remove. Use: /remove_hint hint<ID>")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = str(message.from_user.id)
    chatlogbot.send_message(AUTHORIZED_USER_ID, message.from_user.username + " : " + message.text)

    # Check if the user is in Freeman Mode
    if user_id in users_in_freeman_mode:
        # Handle "Freeman Mode" responses
        if message.text in hints_data["keyword_responses"] and message.text not in users_in_freeman_mode[user_id]["responses_given"]:
            bot.send_message(message.chat.id, hints_data["keyword_responses"][message.text])
            send_to_logbot(f"Bot to User: {hints_data['keyword_responses'][message.text]}")
            users_in_freeman_mode[user_id]["responses_given"].append(message.text)  # Mark response as used
            save_freeman_mode_data(users_in_freeman_mode)  # Save the updated data
        elif message.text in users_in_freeman_mode[user_id]["responses_given"]:
            bot.send_message(message.chat.id, "We’ve already covered that.")
            send_to_logbot("Bot to User: We’ve already covered that.")
        
        # Handle hint requests with cooldown
        elif message.text == "hint":
            current_time = time.time()
            last_hint_time = users_in_freeman_mode[user_id].get("last_hint_time", 0)
    
            # Check if the user is within the cooldown period
            if current_time - last_hint_time < HINT_COOLDOWN:
                remaining_time = int(HINT_COOLDOWN - (current_time - last_hint_time))
                hours, remainder = divmod(remaining_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                bot.send_message(message.chat.id, f"You must wait {hours} hours, {minutes} minutes before asking for another hint.")
                send_to_logbot(f"Bot to User: You must wait {hours} hours, {minutes} minutes before asking for another hint.")
            else:
                # Provide the next unused hint in the list (simple hints first)
                unused_hints = [hint for hint in hints_data["simple_hints"] if hint not in users_in_freeman_mode[user_id]["hints_given"]]
    
                if unused_hints:
                    # Provide the first unused simple hint
                    hint = unused_hints[0]
                    bot.send_message(message.chat.id, hint)
                    send_to_logbot(f"Bot to User: {hint}")
                    # Track the provided hint
                    users_in_freeman_mode[user_id]["hints_given"].append(hint)
                    users_in_freeman_mode[user_id]["last_hint_time"] = current_time  # Update last hint time
                    save_freeman_mode_data(users_in_freeman_mode)  # Save the updated data
                else:
                    bot.send_message(message.chat.id, "You’ve already received all the hints. Time to solve this puzzle on your own!")
                    send_to_logbot("Bot to User: You’ve already received all the hints. Time to solve this puzzle on your own!")

        else:
            bot.send_message(message.chat.id, "I’m afraid I don’t have information on that topic.")
            send_to_logbot(f"Bot to User: I’m afraid I don’t have information on that topic.")
    
    elif message.text == CONTRACT_NUMBER:
        # Activate Freeman Mode for this specific user
        users_in_freeman_mode[user_id] = {"hints_given": [], "responses_given": []}  # Initialize data with empty lists
        save_freeman_mode_data(users_in_freeman_mode)
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}. I see your curiosity led you far. I can answer if you’re on the right path.")
        send_to_logbot(f"Bot to User: Hello, {message.from_user.first_name}. I see your curiosity led you far. I can answer if you’re on the right path.")
    
    elif message.text.replace(" ", "").isdigit():
        # Calculator Mode
        try:
            result = eval(message.text)
            bot.send_message(message.chat.id, f"The answer is: {result}")
            send_to_logbot(f"Bot to User: The answer is: {result}")
        except Exception:
            bot.send_message(message.chat.id, "I can’t process that. Please enter a valid arithmetic expression.")
            send_to_logbot(f"Bot to User: I can’t process that. Please enter a valid arithmetic expression.")
    
    else:
        # Default response for unrecognized messages outside of Freeman Mode
        bot.send_message(message.chat.id, "I don't know who you are and what you want. If you won't type your number, I'll ignore you.")
        send_to_logbot("Bot to User: I don't know who you are and what you want. If you won't type your number, I'll ignore you.")

# Start polling to keep the bot running
while True:
    try:
        bot.polling(timeout=86400, allowed_updates=None)  # Set high timeout and auto-reconnect
    except Exception as e:
        print(f"Bot crashed due to {e}. Restarting in 5 seconds...")
        time.sleep(5)  # Brief pause before restarting
