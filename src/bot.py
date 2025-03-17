import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"

async def send_message(chat_id, text):
    """Function to send a message to a Telegram chat."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": text}
        )
    return response
