from telebot import TeleBot
from telebot.types import Message
from storage import save_user_data, get_user_data  # Import the function
import os
import requests
from docx import Document
import pandas as pd
from functions import audio_video_schedule, insert_into_calendar, save_to_ics
from config import API_TOKEN
user_states = {}

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def initialize_handlers(bot: TeleBot):
    """Registers all bot command handlers."""
    
    @bot.message_handler(commands=['start'])
    def ask_user_details(message: Message):
        """Ask the user for their details."""
        user_id = message.chat.id
        bot.send_message(
            user_id, 
            "👋 Hi! Please send your details in this format:\n\n"
            "**Full Name**\n**Nickname**\n**Group**\n\nExample:\nJohn Doe\nJohnny\nAdmins"
        )
        bot.register_next_step_handler(message, save_user_details)

    def save_user_details(message: Message):
        """Extract and save user details."""
        user_id = message.chat.id
        lines = message.text.split("\n")  # Split the input by newlines
        
        if len(lines) < 3:
            bot.send_message(user_id, "⚠️ Please enter all three details. Try again!")
            bot.register_next_step_handler(message, save_user_details)
            return

        full_name, nickname, group = lines[0], lines[1], lines[2]
        
        # Save user details to JSON file
        save_user_data(user_id, full_name, nickname, group)

        # Send confirmation message
        bot.send_message(
            user_id, 
            f"✅ Saved:\n👤 {full_name}\n🏷️ {nickname}\n📌 {group}"
        )
    
    @bot.message_handler(commands=['upload'])
    def ask_for_document(message):
        bot.send_message(message.chat.id, "Please send me the document you'd like to upload.")

    # Step 2: Handle the uploaded document and register the next step
    @bot.message_handler(content_types=['document'])
    def handle_file_upload(message):
        # Get file information
        
        file_info = bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"
        

        # Download the file
        file_extension = message.document.file_name.split('.')[-1]
        local_filename = f"{UPLOAD_DIR}/{message.document.file_id}.{file_extension}"

        response = requests.get(file_url)
        with open(local_filename, 'wb') as file:
            file.write(response.content)

        bot.send_message(message.chat.id, "File uploaded successfully! Processing...")
                         
        user_id = message.chat.id
        name_to_search = get_user_data(user_id)  # Assuming get_data() is implemented elsewhere

        # Log or print the file name and details
        print("name to search ",name_to_search)

        user_states[user_id] = {
                "file_name": local_filename,
                "name_to_search": name_to_search
            }
        #  # Ask the user to proceed with the next step
        bot.send_message(user_id, "Now that I have received your document, I will process it.")

        file_name = congregation_assignment(user_id)
        # # Register the next step
        bot.send_document(user_id, open(f"uploads/{file_name}", 'rb'))

        
    # Step 3: Define what happens after the document is uploaded (congregation assignment)
    def congregation_assignment(id):
        try:
            # Retrieve the file_name and name_to_search from the user state
            file_name = user_states.get(id, {}).get("file_name")
            name_to_search = user_states.get(id, {}).get("name_to_search")
            
            print(file_name, name_to_search)

            if not file_name and not name_to_search:
                # Perform the next action after receiving the document
                bot.send_message(id, "⚠️ Something went wrong. No data found!")
                
            document = Document(file_name)
            table = document.tables[-1]
            data = [[cell.text for cell in row.cells] for row in table.rows]
            df = pd.DataFrame(data)

            df.columns = df.iloc[1]
        
            df.columns = df.columns.str.replace('\n',' ').str.replace(' ', '_')
            index_found = audio_video_schedule(name_to_search, df)
            calander = insert_into_calendar(index_found, df)
            return save_to_ics(calander)
            # print(calander)
        except Exception as e:
            print(f"Error processing file '{file_name}': {e}")