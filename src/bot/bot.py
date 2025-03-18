from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Welcome to the FastAPI Chatbot.')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Send /start to start the bot.')

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)