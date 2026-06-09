import ssl
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fix SSL certificate verification error
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import os
from datetime import datetime

# Load API key from environment
API_KEY = os.getenv('API_KEY')
CITY = 'Ajax'
COUNTRY_CODE = 'CA'
UNITS = 'metric'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

params = {
    'q': f'{CITY},{COUNTRY_CODE}',
    'appid': API_KEY,
    'units': UNITS
}

try:
    response = requests.get(BASE_URL, params=params, verify=False)
    response.raise_for_status()
    data = response.json()
    
    # Extract weather data
    city = data['name']
    country = data['sys']['country']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description'].capitalize()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Format weather report
    weather_info = f"""## 🌍 Weather Report - Ajax, Ontario, Canada
**Date/Time:** {current_time}

| Metric | Value |
|--------|-------|
| 🌡️ Temperature | {temperature}°C (feels like {feels_like}°C) |
| 💧 Humidity | {humidity}% |
| 🌪️ Wind Speed | {wind_speed} m/s |
| 🎯 Pressure | {pressure} hPa |
| ☁️ Condition | {description} |"""
    
    # Write to file for GitHub Actions
    with open('weather_report.txt', 'w', encoding='utf-8') as f:
        f.write(weather_info)
    
    print("WEATHER_INFO<<EOF")
    print(weather_info)
    print("EOF")
    
except Exception as e:
    print(f"Error fetching weather: {e}")
    exit(1)
