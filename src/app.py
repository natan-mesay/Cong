from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
from dotenv import load_dotenv
import os
from src.bot.handlers import register_handlers
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize FastAPI app
app = FastAPI()

# Initialize Telegram bot application
application = Application.builder().token(TOKEN).build()

# Webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

# Set webhook URL on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    url = "https://cong-acuj.onrender.com"  # Replace with your Render URL
    await application.bot.set_webhook(url)
    register_handlers(application)
    yield
    
    await application.bot.delete_webhook()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)