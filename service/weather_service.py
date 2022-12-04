import requests

def get_weather(latitude,longitude):
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    r = requests.get(url = URL)
    data = r.json()
    weather=data.get("current_weather")
    return weather