from fastapi import FastAPI, Request, BackgroundTasks
from src.bot.bot import updater, bot, TOKEN
from dotenv import load_dotenv

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    updater.start_polling()

@app.post("/webhook")
async def webhook(update: dict, background_tasks: BackgroundTasks):
    updater.dispatcher.process_update(update)
    return "ok"

@app.get("/")
async def read_root():
    return {"message": "Hello, this is the FastAPI Chatbot server."}