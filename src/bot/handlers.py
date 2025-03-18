from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. How can I help you?")

# Command: /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here are the commands you can use:\n/start - Start the bot\n/help - Get help")

# Command: /echo [text]
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)  # Get all arguments after /echo
    await update.message.reply_text(f"You said: {text}")

# Register handlers
def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("echo", echo))