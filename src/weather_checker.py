import requests
import json
import psycopg2
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

#The purpose of this script is to record the actual temperature in each city. The script runs every 30 min and checks which city's time is 12:00pm, so we do not record all 30+ citites time at the same time and get some citites in the middle of the night while other in the afternoon. 

# Database credentials
DB_URI = os.getenv("DB_URI")

# Load cities from cityurl.json
with open('cityurl.json', 'r') as f:
    cities = json.load(f)['cities']

# Scrape temperature from the given URL
def get_temperature(city_url):   
    try:
        response = requests.get(city_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        temp_element = soup.find('div', {'data-testid': 'temperature-text'})
        return temp_element.text.strip() if temp_element else None
    except Exception as e:
        print(f"Error fetching {city_url}: {e}")
        return None

# Convert GMT offset string to a timedelta object
def get_utc_offset(gmt_str):
    sign = 1 if '+' in gmt_str else -1
    parts = gmt_str.replace('+', '').replace('-', '').split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return timedelta(hours=sign * hours, minutes=sign * minutes)

# Check if it's 12:00 local time for any city and update the actual_temperature column
def log_weather_data():
    now_utc = datetime.now(timezone.utc)
    
    for city in cities:
        city_name = city['name']
        city_url = city['url']
        city_gmt = city['gmt']
        
        city_offset = get_utc_offset(city_gmt)
        city_time = now_utc + city_offset
        
        if city_time.hour == 12:
            temp = get_temperature(city_url)
            if temp:
                update_actual_temperature(city_name, city_time.strftime('%Y-%m-%d'), temp)

# Update actual_temperature column in Supabase for the given city and date
def update_actual_temperature(city, date, temperature):
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        cur.execute("""
            UPDATE weather_data
            SET actual_temperature = %s
            WHERE city = %s AND date = %s
        """, (temperature, city, date))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Updated: {city} - {temperature}°C for {date}")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    log_weather_data()
