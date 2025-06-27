import requests
import random

SPOONACULAR_API_KEY = "82dab95e3dda4c93b068c619c5fa2d12"

def get_recipes(query, dietary):
    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {        
        "query": query,
        "diet": dietary,
        "number": 8,
        "apiKey": SPOONACULAR_API_KEY,
        "addRecipeInformation": True
        }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return None

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_based_query(temp, n=3):
    if temp < 15:
        options = [
            "soup", "stew", "curry", "chili", "bake", "lasagna", "shepherd's pie",
            "ramen", "hotpot", "casserole", "pot roast", "gnocchi", "risotto"
        ]
    elif temp > 25:
        options = [
            "salad", "smoothie", "wrap", "cold pasta", "sandwich", "poke bowl",
            "sushi", "gazpacho", "ceviche", "fruit salad", "spring rolls", "tacos"
        ]
    else:
        options = [
            "pasta", "rice", "stir fry", "grill", "pizza", "quiche", "paella",
            "burrito", "frittata", "omelette", "shakshuka", "couscous", "noodles"
        ]
    return random.sample(options, min(n, len(options)))

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        "apiKey": SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)
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