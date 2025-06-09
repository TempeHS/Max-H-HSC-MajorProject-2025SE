import requests
OPENWEATHER_API_KEY = "1c7653cfb4f11ede9ba7fa6bd8e84769"

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def get_weather_based_dish(temp, weather_desc):
    if temp is None:
        return "Weather data unavailable."
    if temp < 10:
        return "It's cold! Warm soups, stews, and casseroles are perfect."
    elif temp > 25:
        return "It's hot! Try salads, cold dishes, or grilled foods."
    elif "rain" in weather_desc.lower():
        return "Rainy weather calls for comfort food like pasta or curry."
    else:
        return "Mild weather is great for any dish—try something seasonal!"