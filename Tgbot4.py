import telebot
import subprocess
import os

# Bot token and authorized user ID for updates
TOKEN = 'YOUR_BOT_TOKEN'
AUTHORIZED_USER_ID = 123456789  # Replace with your Telegram user ID for updates

# Contract number and predefined responses in Freeman Mode
CONTRACT_NUMBER = '413'
freeman_mode = False
responses = {
    "diary": "Oh, you want to see my diary? I bet you already know where it is. The key to decrypt those files is: influenceproject",
    "hint": "Remember, the truth lies in the numbers. Start with CBC 128 encryption.",
    "code": "The company hides more than it shows. Watch out for subtle messages."
}
used_responses = set()  # Tracks used responses

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to SyncraHelperBot. I’m here to assist you with basic calculations. Send me a math problem!")

@bot.message_handler(commands=['update'])
def update_bot(message):
    # Only allow the authorized user to run updates
    if message.from_user.id == AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "Checking for updates...")
        try:
            # Pull the latest changes from the GitHub repo and restart the bot
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
            bot.send_message(message.chat.id, "Bot updated successfully.")
            # Restart the bot (this example uses a simple way; you might need a more sophisticated setup depending on hosting)
            os.execv(__file__, ['python'] + sys.argv)
        except subprocess.CalledProcessError:
            bot.send_message(message.chat.id, "Failed to update the bot. Please check the repository.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to update the bot.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global freeman_mode
    
    if freeman_mode:
        # Handle "Freeman Mode" responses
        if message.text in responses and message.text not in used_responses:
            bot.send_message(message.chat.id, responses[message.text])
            used_responses.add(message.text)
        elif message.text in used_responses:
            bot.send_message(message.chat.id, "We’ve already covered that.")
        else:
            bot.send_message(message.chat.id, "I’m afraid I don’t have information on that topic.")
    
    elif message.text == CONTRACT_NUMBER:
        # Activate Freeman Mode
        freeman_mode = True
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}. I see your curiosity led you far. I can answer if you’re on the right path.")
    
    elif message.text.replace(" ", "").isdigit():
        # Calculator Mode
        try:
            result = eval(message.text)
            bot.send_message(message.chat.id, f"The answer is: {result}")
        except Exception:
            bot.send_message(message.chat.id, "I can’t process that. Please enter a valid arithmetic expression.")
    
    else:
        # If no valid action is found
        bot.send_message(message.chat.id, "I don't know who you are and what you want. If you won't type your number, I'll ignore you.")

# Start polling to keep the bot running
bot.polling()
