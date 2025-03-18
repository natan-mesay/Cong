import telebot
from config import API_TOKEN
from handlers import initialize_handlers
from database import create_table
# Initialize bot
bot = telebot.TeleBot(API_TOKEN)

# Register handlers
initialize_handlers(bot)
create_table()
# Start the bot
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling()
