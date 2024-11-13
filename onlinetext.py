from telethon.sync import TelegramClient
from telethon import events
import os

# Your API ID, API hash, and phone number
api_id = '25583069'  # Replace with your actual api_id
api_hash = 'ead2f37b8ce17ef8dbe6a25cb42ad786'  # Replace with your actual api_hash
phone = '+37379171154'  # Replace with your phone number

# The path to your document
document_path = 'Plan.pdf'  # Make sure this file exists in your directory

# Create a Telegram session
client = TelegramClient('session', api_id, api_hash)

# Connect and authorize with your phone number
client.connect()

# If not authorized, sign in
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# Event handler for receiving new messages
@client.on(events.NewMessage)
async def handler(event):
    # Check if the received message is "Send me the plan"
    if event.text.lower() == "send me the plan":
        # Send the document to the user
        await event.reply(file=document_path)
        print(f"Sent 'Plan.pdf' to {event.sender_id}")
    else:
        print(f"Received message: {event.text}")

@client.on(events.UserUpdate)
async def onlinehandler(event):
    user = await client.get_entity(event.user_id)
    username = user.username if user.username else str(user.id)  # Fallback to user ID if no username
    user = await client.get_entity(event.user_id)
    # Log the event received with the username and event type (status or action)
    if event.status:
        if event.status == 'online':
            # User came online
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{username}] : online")
            # Optionally, send the time to the user
            await client.send_message(event.user_id, f"Hello! The current time is: {current_time}")
            print(f"Sent time to {username} at {current_time}")
        elif event.status == 'offline':
            # User went offline
            print(f"[{username}] : offline")
        else:
            print(f"[{username}] : status updated: {event.status}")
    elif event.action == 'typing':
        # User is typing
        print(f"[{username}] : typing")
    if user.username == "dyyona":
        await client.send_message(event.user_id, "Я вижу что ты в сети")

# Start listening for incoming messages
print("Bot is running and listening for messages...")
client.run_until_disconnected()

# Disconnect the session when done
client.disconnect()
