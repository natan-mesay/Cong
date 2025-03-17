import os
import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = FastAPI()

class Information(BaseModel):
    name: str
    nick_name: str
    group: str
    
class TelegramUpdate(BaseModel):
    message: dict
    
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/webhook")
async def receive_update(update: TelegramUpdate):
    """Handles incoming updates from Telegram"""
    chat_id = update.message["chat"]["id"]
    text = update.message["text"]

    response_text = f"You said: {text}"
    async with httpx.AsyncClient() as client:
        await client.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": response_text})

    return {"status": "ok"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/information")
def store_information(information: Information):
    print(f"Information received: {information}")
    return {"message": "Information stored successfully"}
    
    