from telethon.sync import TelegramClient
from telethon import events
from telethon.tl.types import UserStatusOnline, UserStatusOffline
import datetime
import os

api_id = '25583069'  # Replace with your actual api_id
api_hash = 'ead2f37b8ce17ef8dbe6a25cb42ad786'  # Replace with your actual api_hash
phone = '+37379171154'  # Replace with your phone number

requser = input("user to message: ")

document_path = 'Plan.pdf'  

client = TelegramClient('session', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

@client.on(events.NewMessage)
async def handler(event):
    if event.text.lower() == "send me the plan":
        await event.reply(file=document_path)
        print(f"Sent 'Plan.pdf' to {event.sender_id}")
    else:
        print(f"Received message: {event.text}")

@client.on(events.UserUpdate)
async def onlinehandler(event):
    user = await client.get_entity(event.user_id)
    username = user.username if user.username else str(user.id)  # Fallback to user ID if no username
    user = await client.get_entity(event.user_id)
    
    if event.status:
        if event.online:
            # User came online
            print(f"[{username}] : online")
        #elif event.offline:
            # User went offline
            #print(f"[{username}] : offline")
        #elif event.action == 'typing':
            # User is typing
            #print(f"[{username}] : typing")
        elif isinstance(event.status, UserStatusOffline):
            print(f"[{username}] : offline")
            if user.username== requser:
                await client.send_message(event.user_id, "Don't go offline, please, I'll miss you 😥")
        else:
            print(f"[{username}] : status updated: {event.status}")
    if user.username == requser and event.online:
        await client.send_message(event.user_id, "Howdy? 😊")
    if user.username == requser and event.typing:
        await client.send_message(event.user_id, "😶")

print("Bot is running and listening for messages...")
client.run_until_disconnected()

client.disconnect()
