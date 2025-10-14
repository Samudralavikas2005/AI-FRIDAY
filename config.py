# config.py
import os

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash-lite"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"
CALENDARIFIC_API_KEY = os.getenv("CALENDARIFIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# File Paths
MEMORY_FILE = "friday_memory.json"
REMINDER_FILE = "reminders.json"
STUDY_PLAN_FILE = "study_plan.json"
CONTACTS_FILE = "contacts.json"

# Email Configuration - USING OS ENVIRONMENT VARIABLES
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': os.getenv("SENDER_MAIL"),  # From .bashrc
    'sender_password': os.getenv("SENDER_PASSWORD")  # From .bashrc
}

# Other Configuration
COUNTRY_CODE = "IN"
