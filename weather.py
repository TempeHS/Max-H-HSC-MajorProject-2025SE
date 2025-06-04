import requests
OPENWEATHER_API_KEY = "1c7653cfb4f11ede9ba7fa6bd8e84769"

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None