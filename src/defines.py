import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
