import requests

from dotenv import load_dotenv, find_dotenv, get_key
load_dotenv()

WEATHER_API_KEY = get_key(find_dotenv(), "WEATHER_API_KEY")

def get_weather(city, date):
    url = f"https://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={city}&dt={date}"
    res = requests.get(url, timeout=10)
    return res.json() if res.status_code == 200 else None
