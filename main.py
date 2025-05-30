
import os
import threading
import requests
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Loads values from .env

# Telegram Bot API Credentials (securely loaded)
API_ID = int(os.getenv("API_ID",""))
API_HASH = os.getenv("API_HASH","")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID","1773034985"))
API_URL = os.getenv("API_URL")

# MongoDB Connection
MONGO_URL = "mongodb+srv://montukaka818:montukaka818@cluster0.gh5kx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client["TruecallerBot"]
users_collection = db["users"]


# Image URL for Start Message
START_IMAGE = "https://envs.sh/Q0_.jpg"

# Caption with Bot Features
START_CAPTION = """\
┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼──────• 
│◍ Hello Everyone,
│◍ [ᴛʜɪs ɪs ᴛʀᴜᴇᴄᴀʟʟᴇʀʙᴏᴛ ʙʏ ༄ᶦᶰᵈ᭄࿐𝘗𝘢𝘳𝘢𝘥𝟎𝘹](https://t.me/pArAd0X6)
└──────────────────────•

•──────────────────────•
**Features:**
◍ **Nᴜᴍʙᴇʀ Lᴏᴏᴋᴜᴘ** – Cᴀʟʟᴇʀ ᴋᴀ ɴᴀᴀᴍ ᴀᴜʀ ᴅᴇᴛᴀɪʟs ᴘᴀᴛᴀ ᴋᴀʀᴇ.
◍ **Bᴜʟᴋ Sᴇᴀʀᴄʜ** – Eᴋ sᴀᴛʜ ᴍᴜʟᴛɪᴘʟᴇ ɴᴜᴍʙᴇʀs ᴄʜᴇᴄᴋ ᴋᴀʀᴇ.
◍ **Pʀɪᴠᴀᴄʏ Sᴀғᴇ** – Usᴇʀ ᴅᴀᴛᴀ sᴇᴄᴜʀᴇ ᴀᴜʀ ᴘʀɪᴠᴀᴛᴇ ʀᴀʜᴇ.
•──────────────────────•
❖ 𝐏ᴏᴡᴇʀᴇᴅ ʙʏ ➟ [༄ᶦᶰᵈ᭄࿐𝘗𝘢𝘳𝘢𝘥𝟎𝘹](https://t.me/pArAd0X6)
•──────────────────────•
"""

# Initialize Telegram Bot
bot = Client("truecaller_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
def start(_, message):
    user_id = message.from_user.id
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/pArAd0X6")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/world_of_pardox76"),
         InlineKeyboardButton("ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/world_0f_parad0x")]
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
 **ɴᴜᴍʙᴇʀ:** {data.get('international_format', 'N/A')}
**ᴄᴏᴜɴᴛʀʏ:** {data.get('location', 'N/A')}

**🔍 𝖳𝗋𝗎𝖾𝖼𝖺𝗅𝗅𝖾𝗋 𝖲𝖺𝗒𝗌 :**

**Name:** {data.get('Unknown', 'No name found')}
**ᴄᴏᴜɴᴛʀʏ:** {data.get('carrier', 'N/A')}
**ʟᴏᴄᴀᴛɪᴏɴ:** {', '.join(data.get('timezones', []))}

**🔍 𝖴𝗇𝗄𝗇𝗈𝗐𝗇 𝖲𝖺𝗒𝗌 :**
**ᴜɴᴋɴᴏᴡɴ ᴅᴀᴛᴀ:** {data.get('Unknown', 'N/A')}

[𝗪𝗵𝗮𝘁𝘀𝗮𝗽𝗽](https://wa.me/{phone_number}) | [𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺](https://t.me/{phone_number})
        """
    else:
        result = "❌ 𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝖿𝖾𝗍𝖼𝗁 𝖽𝖺𝗍𝖺. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗅𝖺𝗍𝖾𝗋."
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
    app.run(host="0.0.0.0", port=8080)

# Run Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start the Telegram bot
bot.run()
