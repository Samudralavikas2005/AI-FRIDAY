# utilities/weather.py
import requests
from config import WEATHER_API_KEY

class WeatherService:
    def __init__(self):
        pass
    
    def get_weather(self, city):
        if not WEATHER_API_KEY:
            return "Weather API key not set. Please configure WEATHER_API_KEY."
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if data.get("cod") != 200:
                return f"Sorry, I couldn't find weather info for {city}."
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            return f"The weather in {city} is {desc} with {temp}°C, feels like {feels_like}°C."
        except Exception as e:
            return f"Sorry, I couldn't fetch weather info. Error: {e}"
