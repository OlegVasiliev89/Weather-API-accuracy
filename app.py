import requests
import psycopg2
from datetime import datetime, timedelta
from flask import Flask, jsonify
import json

# The purpose of this script is to record the weather for spesific cities in 2 days via 3 diffrent weather APIs to see which API is more accurate for which area of the world

app = Flask(__name__)

# Database setup
DB_URI = 'postgresql://postgres:********!@db.********.supabase.co:5432/postgres'
conn = psycopg2.connect(DB_URI)
cursor = conn.cursor()

# API keys and URLs
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"
OPENWEATHER_API_KEY = "*********"

WEATHERBIT_URL = "https://api.weatherbit.io/v2.0/forecast/daily"
WEATHERBIT_API_KEY = "***********"

WEATHERAPI_URL = "http://api.weatherapi.com/v1/forecast.json"
WEATHERAPI_API_KEY = "********"

# Load city data from JSON file
with open('apicities.json') as f:
    cities = json.load(f)

# Function to create the table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        date DATE,
        city VARCHAR(255),
        actual_temperature FLOAT,
        openweather_forecast FLOAT,
        openweather_accuracy FLOAT,
        openweather_accuracy_avg FLOAT,
        weatherbit_forecast FLOAT,
        weatherbit_accuracy FLOAT,
        weatherbit_accuracy_avg FLOAT,
        weatherapi_forecast FLOAT,
        weatherapi_accuracy FLOAT,
        weatherapi_accuracy_avg FLOAT
    )
""")
conn.commit()

# Function to fetch weather forecast from APIs
def get_openweather_forecast(lat, lon, days_ahead):
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(OPENWEATHER_URL, params=params)
    data = response.json()
    
    for forecast in data['list']:
        dt = datetime.utcfromtimestamp(forecast['dt'])
        if dt.date() == (datetime.utcnow() + timedelta(days=days_ahead)).date() and dt.hour == 12:
            return forecast['main']['temp']

def get_weatherbit_forecast(lat, lon, days_ahead):
    params = {
        'lat': lat,
        'lon': lon,
        'key': WEATHERBIT_API_KEY,
        'units': 'M'
    }
    response = requests.get(WEATHERBIT_URL, params=params)
    data = response.json()
    
    if 'data' in data and len(data['data']) > days_ahead:
        return data['data'][days_ahead]['temp']
    return None

def get_weatherapi_forecast(lat, lon, days_ahead):
    params = {
        'q': f'{lat},{lon}',
        'key': WEATHERAPI_API_KEY,
        'days': 3
    }
    response = requests.get(WEATHERAPI_URL, params=params)
    data = response.json()
    
    if 'forecast' in data and 'forecastday' in data['forecast']:
        if days_ahead < len(data['forecast']['forecastday']):
            return data['forecast']['forecastday'][days_ahead]['day']['avgtemp_c']
    return None

# Function to save data to the database
def save_weather_data(city_name, openweather_forecast, weatherbit_forecast, weatherapi_forecast, days_ahead):
    forecast_date = (datetime.now() + timedelta(days=days_ahead)).date()
    cursor.execute("""
        INSERT INTO weather_data (
            date, city, openweather_forecast, weatherbit_forecast, weatherapi_forecast,
            openweather_accuracy, weatherbit_accuracy, weatherapi_accuracy,
            openweather_accuracy_avg, weatherbit_accuracy_avg, weatherapi_accuracy_avg
        ) VALUES (%s, %s, %s, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)
    """, (forecast_date, city_name, openweather_forecast, weatherbit_forecast, weatherapi_forecast))
    conn.commit()

@app.route('/update_weather')
def update_weather():
    days_ahead = 2  # Day after tomorrow
    
    for city in cities:
        city_name = city['name']
        lat = city['lat']
        lon = city['lon']
        
        openweather_forecast = get_openweather_forecast(lat, lon, days_ahead)
        weatherbit_forecast = get_weatherbit_forecast(lat, lon, days_ahead)
        weatherapi_forecast = get_weatherapi_forecast(lat, lon, days_ahead)
        
        if openweather_forecast is not None and weatherbit_forecast is not None and weatherapi_forecast is not None:
            save_weather_data(city_name, openweather_forecast, weatherbit_forecast, weatherapi_forecast, days_ahead)

    return jsonify({"message": "Weather data updated successfully!"})

if __name__ == '__main__':
    app.run(debug=True)