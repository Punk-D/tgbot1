from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon import events
import random
import time

# Your API ID, API hash, and phone number
api_id = '25583069'  # Replace with your actual api_id
api_hash = 'ead2f37b8ce17ef8dbe6a25cb42ad786'  # Replace with your actual api_hash
phone = '+37379171154'  # Replace with your phone number

phrases = [
    "Hey there! Hope you're having a great day!",
    "Just checking in—how's everything going?",
    "You’re doing awesome! Keep it up!",
    "Hope you're feeling good today!",
    "Sending positive vibes your way!",
    "Stay awesome, my friend!",
    "Keep shining, you're doing great!",
    "You’ve got this—keep going!",
    "Hello! Wishing you a fantastic day ahead!",
    "Just a little reminder: you're amazing!",
    "I believe in you—don't stop!",
    "Hope your day is as amazing as you are!",
    "Remember, you are capable of incredible things!",
    "Take a moment for yourself today—you're worth it!",
    "Keep smiling, you're doing great!",
    "Every step forward is progress—keep it up!",
    "Good vibes only—let’s make today awesome!",
    "You're stronger than you think!",
    "The world is better with you in it!",
    "Sending some love your way today!"
]

# Create a Telegram session
client = TelegramClient('session', api_id, api_hash)

# Connect and authorize with your phone number
client.connect()

# If not authorized, sign in
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# Get the user entity (replace 'username_or_phone' with the actual username or phone number)
username_or_phone = input("Input username to send the message to : ")  # Replace with actual username or phone number
user = client.get_entity(username_or_phone)

# Get the user ID and access hash
user_id = user.id
access_hash = user.access_hash

# Print the user ID and access hash
print(f"User ID: {user_id}, Access Hash: {access_hash}")

# Create the InputPeerUser object
receiver = InputPeerUser(user_id, access_hash)

# Function to handle incoming messages
@client.on(events.NewMessage)
async def my_event_handler(event):
    # Check if the message is from the user we're interacting with and if it matches "Text me bot"
    if event.sender_id == user_id and event.text == "Text me bot":
        # Choose a random phrase from the list
        response = random.choice(phrases)
        # Send the message to the user
        await client.send_message(receiver, response, parse_mode='html')
        print(f"Sent random message: {response}")

# Run the client and start listening for messages
print("Bot is running and waiting for a message...")
client.run_until_disconnected()

# Disconnect the session when done (this will never run unless the bot is stopped manually)
client.disconnect()
