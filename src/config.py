import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Telegram Bot Token
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is missing. Check your .env file.")
