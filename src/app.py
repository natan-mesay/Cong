from fastapi import FastAPI, HTTPException, Request
from telegram import Update
from telegram.ext import Application
from dotenv import load_dotenv
import os
from src.bot.handlers import register_handlers
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize FastAPI app
app = FastAPI()

# Initialize Telegram bot application
application = Application.builder().token(TOKEN).build()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
# Webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        logger.info(f"Incoming update: {data}")  # Log the incoming update

        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

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