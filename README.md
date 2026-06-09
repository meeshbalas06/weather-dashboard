# Weather Dashboard

A Python weather dashboard that fetches real-time weather data for Ajax, Ontario using the OpenWeatherMap API. Includes automated daily weather reports via GitHub Actions.

## Features

- ✅ Fetches real-time weather data from OpenWeatherMap
- ✅ Displays temperature, humidity, wind speed, and weather conditions
- ✅ Automated daily weather reports at 9 AM EST (creates GitHub issues)
- ✅ Easy to configure for different locations
- ✅ Handles SSL certificate verification automatically

## Prerequisites

- Python 3.7+
- OpenWeatherMap API key (get it for free at https://openweathermap.org/api)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/meeshbalas06/weather-dashboard.git
cd weather-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Create a `.env` file in the project root
   - Add your OpenWeatherMap API key:
   ```
   API_KEY=your_api_key_here
   ```

## Usage

### Manual Weather Report

Run the weather dashboard to get current weather:
```bash
python weather.py
```

This will display the current weather for Ajax, Ontario in your terminal.

### Automated Daily Reports

Set up GitHub Actions to automatically create weather reports at **9 AM EST every day**:

1. **Add your API key as a GitHub secret:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `OPENWEATHER_API_KEY`
   - Value: paste your OpenWeatherMap API key

2. **Create the workflow file:**
   - Create folder: `.github/workflows/`
   - Create file: `.github/workflows/daily-weather-report.yml`
   - Copy the workflow content (see [workflow template](#workflow-template))
   - Commit and push

3. **That's it!** At 9 AM EST every day, a GitHub Issue will be created with the weather report.

You can also manually trigger the workflow from the Actions tab anytime.

### Workflow Template

Create `.github/workflows/daily-weather-report.yml`:

```yaml
name: Daily Weather Report

on:
  schedule:
    # Runs at 9 AM EST (2 PM UTC) every day
    - cron: '0 14 * * *'
  workflow_dispatch:  # Allow manual triggering

jobs:
  weather-report:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Fetch weather data
        id: weather
        env:
          API_KEY: ${{ secrets.OPENWEATHER_API_KEY }}
        run: |
          python -c "
import requests
import os
from datetime import datetime
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

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

response = requests.get(BASE_URL, params=params, verify=False)
data = response.json()

city = data['name']
country = data['sys']['country']
temperature = data['main']['temp']
feels_like = data['main']['feels_like']
humidity = data['main']['humidity']
pressure = data['main']['pressure']
wind_speed = data['wind']['speed']
description = data['weather'][0]['description'].capitalize()
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

weather_info = f'''
## 🌍 Weather Report - Ajax, Ontario, Canada
**Date/Time:** {current_time}

| Metric | Value |
|--------|-------|
| 🌡️ Temperature | {temperature}°C (feels like {feels_like}°C) |
| 💧 Humidity | {humidity}% |
| 🌪️ Wind Speed | {wind_speed} m/s |
| 🎯 Pressure | {pressure} hPa |
| ☁️ Condition | {description} |
'''

print('WEATHER_INFO<<EOF')
print(weather_info)
print('EOF')
          "
      
      - name: Create GitHub Issue
        uses: actions/github-script@v6
        with:
          script: |
            const weatherInfo = `${{ steps.weather.outputs.WEATHER_INFO }}`;
            
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Daily Weather Report - ${new Date().toLocaleDateString()}`,
              body: weatherInfo,
              labels: ['weather-report']
            });
```

## Configuration

### Change Location

To get weather for a different city, edit `weather.py`:

```python
CITY = "Toronto"        # Change to your city
COUNTRY_CODE = "CA"     # Change to your country code
```

### Change Time

To change the automation time, edit the cron schedule in `.github/workflows/daily-weather-report.yml`:

```yaml
- cron: '0 14 * * *'    # 9 AM EST (2 PM UTC)
```

[Cron format reference](https://crontab.guru/)

## API Reference

- Uses [OpenWeatherMap Current Weather API](https://openweathermap.org/current)
- City: Ajax, Ontario, Canada
- Units: Metric (Celsius)
- Updates: Real-time

## Files

- `weather.py` - Main script to fetch and display weather
- `requirements.txt` - Python dependencies
- `.env` - API key configuration (not committed to repo)
- `.gitignore` - Excludes sensitive files
- `.github/workflows/daily-weather-report.yml` - GitHub Actions automation

## Troubleshooting

### SSL Certificate Error

If you get an SSL error, make sure you're using the latest `weather.py` which includes SSL fixes.

### API Key Not Found

- Check that `.env` file exists in the project root
- Verify the format: `API_KEY=your_key_here` (no spaces, no quotes)
- Make sure you have `pip install python-dotenv`

### 401 Unauthorized

- Your API key is invalid or hasn't been activated yet
- Wait 5-10 minutes after creating the key
- Try generating a new key from https://openweathermap.org/api

## License

MIT
