import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
DISCORD_TARGET_CHANNEL_ID = int(os.getenv('DISCORD_TARGET_CHANNEL_ID'))
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
