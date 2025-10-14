# utilities/calendar.py
import datetime
import requests
from config import CALENDARIFIC_API_KEY, COUNTRY_CODE

class CalendarService:
    def __init__(self):
        pass
    
    def get_important_days(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        if not CALENDARIFIC_API_KEY:
            return "Calendarific API key not set. Please configure CALENDARIFIC_API_KEY."
        try:
            url = f"https://calendarific.com/api/v2/holidays?&api_key={CALENDARIFIC_API_KEY}&country={COUNTRY_CODE}&year={datetime.date.today().year}&month={datetime.date.today().month}&day={datetime.date.today().day}"
            response = requests.get(url, timeout=10).json()
            holidays = response.get("response", {}).get("holidays", [])
            if not holidays:
                return "There are no important days today."
            names = [h['name'] for h in holidays]
            return "Today is special: " + ", ".join(names)
        except Exception as e:
            return f"Could not fetch important days. Error: {e}"
