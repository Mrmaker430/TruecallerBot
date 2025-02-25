import threading
import requests
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# Telegram Bot API Credentials
API_ID = 14050586
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"
BOT_TOKEN = "7784061051:AAHXad6hJ0SNWn5MDR8SZuHE_le5wCqqI-s"
OWNER_ID = 6258915779  # Change to int (remove quotes)

# MongoDB Connection
MONGO_URL = "mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["TruecallerBot"]
users_collection = db["users"]

# Truecaller API Endpoint
API_URL = "https://worm.ytansh038.workers.dev/?number="

# Image URL for Start Message
START_IMAGE = "https://envs.sh/Q0_.jpg"

# Caption with Bot Features
START_CAPTION = """\
┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼──────• 
│◍ Hello Everyone,
│◍ [ᴛʜɪs ɪs ᴛʀᴜᴇᴄᴀʟʟᴇʀʙᴏᴛ ʙʏ Aɴsʜ](https://t.me/cyber_ansh)
└──────────────────────•
...
"""

# Initialize Telegram Bot
bot = Client("truecaller_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
def start(_, message):
    user_id = message.from_user.id
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/cyber_ansh")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/+QAn371T81bc0MGY1"),
         InlineKeyboardButton("ᴀᴘɪ ᴄʜᴀɴɴᴇʟ", url="https://t.me/+7AUuVrP8F69kYWY1")]
    ])
    
    message.reply_photo(
        photo=START_IMAGE,
        caption=START_CAPTION,
        reply_markup=keyboard
    )

@bot.on_message(filters.text & filters.private)
def fetch_number_details(_, message):
    phone_number = message.text.strip()
    if not phone_number.startswith("+"):
        phone_number = "+91" + phone_number

    response = requests.get(API_URL + phone_number)
    if response.status_code == 200:
        data = response.json()
        result = f"""
📞 **Phone Number:** {data.get('international_format', 'N/A')}
📡 **Carrier:** {data.get('carrier', 'N/A')}
🌍 **Location:** {data.get('location', 'N/A')}
⏳ **Timezone:** {', '.join(data.get('timezones', []))}
🔍 **Truecaller Name:** {data.get('Truecaller', 'No name found')}
❓ **Unknown Data:** {data.get('Unknown', 'N/A')}
        """
    else:
        result = "❌ Failed to fetch data. Please try again later."
    message.reply_text(result)

@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
def broadcast(_, message):
    text = message.text.split(" ", 1)
    if len(text) < 2:
        message.reply_text("Usage: /broadcast Your message here")
        return
    broadcast_message = text[1]
    users = users_collection.find()
    count = 0
    for user in users:
        try:
            bot.send_message(user["user_id"], broadcast_message)
            count += 1
        except:
            pass
    message.reply_text(f"✅ Broadcast sent to {count} users.")

# Flask Web Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Truecaller Bot is Running!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Run Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start the Telegram bot
bot.run()
