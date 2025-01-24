import os
from dotenv import load_dotenv

dotenv_path = '../backend/.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)