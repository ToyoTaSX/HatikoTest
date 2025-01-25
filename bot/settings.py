import os
from dotenv import load_dotenv
dotenv_path = '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
BOT_API_USERNAME = os.getenv('BOT_API_USERNAME')
BOT_API_PASSWORD = os.getenv('BOT_API_PASSWORD')
API_URL='http://127.0.0.1:8000/'
ADMINS = [791396692]
TIMEZONE = 'Europe/Moscow'