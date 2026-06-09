import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY = os.getenv('API_KEY')
CITY = "Ajax"
COUNTRY_CODE = "CA"
UNITS = "metric"  # Use Celsius

# OpenWeatherMap API endpoint
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather():
    """Fetch current weather data from OpenWeatherMap API"""
    
    if not API_KEY:
        print("Error: API_KEY not found. Please set it in your .env file")
        return None
    
    # Parameters for the API request
    params = {
        'q': f"{CITY},{COUNTRY_CODE}",
        'appid': API_KEY,
        'units': UNITS
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather(data):
    """Display weather information in a formatted way"""
    
    if not data:
        return
    
    # Extract relevant data
    city = data['name']
    country = data['sys']['country']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description'].capitalize()
    icon = data['weather'][0]['icon']
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display the weather information
    print("\n" + "="*50)
    print(f"🌍 WEATHER DASHBOARD - {current_time}")
    print("="*50)
    print(f"📍 Location: {city}, {country}")
    print(f"🌡️  Temperature: {temperature}°C (feels like {feels_like}°C)")
    print(f"💧 Humidity: {humidity}%")
    print(f"🌪️  Wind Speed: {wind_speed} m/s")
    print(f"🎯 Pressure: {pressure} hPa")
    print(f"☁️  Condition: {description}")
    print("="*50 + "\n")

def main():
    """Main function to run the weather dashboard"""
    print("Fetching weather data for Ajax, Ontario, Canada...")
    weather_data = fetch_weather()
    display_weather(weather_data)

if __name__ == "__main__":
    main()
