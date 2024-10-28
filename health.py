from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("GitHub token not found. Make sure it's set in the .env file.")
else:
    print("GitHub token loaded successfully.")
