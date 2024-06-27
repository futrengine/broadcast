from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Constants
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))  # Ensure this is an integer

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# List to store user IDs who started the bot
user_ids = []

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user_ids.append(message.from_user.id)
    await message.reply_photo(
        photo="path_to_welcome_image.jpg",  # Replace with the path to your welcome image
        caption=f"Hello {message.from_user.mention}, I am a helper for my owner for broadcasting."
    )

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client: Client, message: Message):
    broadcast_message = message.reply_to_message
    if not broadcast_message:
        await message.reply("Reply to a message to broadcast it.")
        return

    for user_id in user_ids:
        try:
            if broadcast_message.photo:
                await client.send_photo(user_id, broadcast_message.photo.file_id, caption=broadcast_message.caption)
            elif broadcast_message.poll:
                await client.send_poll(
                    chat_id=user_id,
                    question=broadcast_message.poll.question,
                    options=[option.text for option in broadcast_message.poll.options]
                )
            else:
                await client.send_message(user_id, broadcast_message.text)
        except Exception as e:
            logging.error(f"Failed to send message to {user_id}: {e}")

@app.on_message(filters.command("addadmin") & filters.user(ADMIN_ID))
async def add_admin(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /addadmin <user_id>")
        return

    new_admin_id = int(message.command[1])
    global ADMIN_ID
    ADMIN_ID = new_admin_id
    await message.reply(f"Admin rights granted to user ID: {new_admin_id}")

if __name__ == "__main__":
    app.run()