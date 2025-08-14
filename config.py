
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8319690083:AAEkvCv8Pj8jTMMBsqd27IV0ZZdOTNfGC0Q")
GOOGLE_SHEET_ID = os.getenv("1Bg2TSHhnI9Z1vvC6v0bpCL6QwczVzbwd4lGizmwdlwo")
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN")
ROBOKASSA_PASSWORD = os.getenv("ROBOKASSA_PASSWORD")
GOOGLE_CREDS_PATH = "/opt/render/project/src/google_creds.json"