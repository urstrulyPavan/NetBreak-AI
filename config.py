import os
from dotenv import load_dotenv
load_dotenv()
APP_TITLE = "NetBreak AI"
APP_TAGLINE = "Break. Investigate. Fix. Learn."
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
