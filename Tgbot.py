from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser

# Your API ID, API hash, and phone number
api_id = '25583069'  # Replace with your actual api_id
api_hash = '8158170604:AAHzUDShobxPIDwB-9xRFTyIkuAF8K4-NpQ'  # Replace with your actual api_hash
phone = '+37379171154'  # Replace with your phone number
message = input("input message to be sent : ")  # Message to send

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

try:
    # Send the message to the user
    client.send_message(receiver, message, parse_mode='html')
    print("Message sent successfully!")
except Exception as e:
    # Handle any errors (e.g., wrong user ID, access hash, etc.)
    print(f"Error occurred: {e}")

# Disconnect the session
client.disconnect()
