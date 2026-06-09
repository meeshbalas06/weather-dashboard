# Weather Dashboard

A simple Python weather dashboard that fetches current weather data for Ajax, Ontario using the OpenWeatherMap API.

## Features

- Fetches real-time weather data from OpenWeatherMap
- Displays temperature, humidity, wind speed, and weather conditions
- Easy to configure for different locations

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

Run the weather dashboard:
```bash
python weather.py
```

This will display the current weather for Ajax, Ontario.

## API Reference

- Uses OpenWeatherMap Current Weather API
- City: Ajax, Ontario, Canada
- Updates: Real-time

## License

MIT
