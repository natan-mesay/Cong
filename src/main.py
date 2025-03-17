from fastapi import FastAPI, Depends
from src.bot import send_message
from src.models import TelegramMessage

app = FastAPI()

@app.post("/send-message")
async def send_telegram_message(message: TelegramMessage):
    """Route to send message to Telegram chat."""
    response = await send_message(message.chat_id, message.text)
    return {"status": "ok", "response": response.json()}
