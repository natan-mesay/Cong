import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://cong-acuj.onrender.com/webhook"

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
response = requests.get(url)

if response.status_code == 200:
    print("Webhook set successfully")
else:
    print("Failed to set webhook")