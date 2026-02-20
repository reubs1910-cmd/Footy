import os
from dotenv import load_dotenv

# Config file to load API key

load_dotenv() # reads env file and sets up environment variables

FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")