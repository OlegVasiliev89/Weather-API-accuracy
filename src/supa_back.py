from flask_cors import CORS
from flask import Flask, jsonify
import psycopg2
import json
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# The purpose of this backend is to service the web app that presents the data from the Supabase DB and let the user see most recent averages for temperature accuracy over 3 weather APIs

# Flask app
app = Flask(__name__)
CORS(app)

# Supabase Database connection settings
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")  

# Function to connect to Supabase
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Function to fetch data from Supabase and save as JSON
def generate_json_file():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, date, openweather_accuracy_avg, weatherbit_accuracy_avg, weatherapi_accuracy_avg
        FROM weather_data
        WHERE date = CURRENT_DATE - INTERVAL '1 day'
    """)
    rows = cursor.fetchall()

    # Convert database rows to JSON format
    cities_data = [
        {
            "city_name": row[0],
            "date": row[1].isoformat(),
            "openweather_accuracy_avg": row[2],
            "weatherbit_accuracy_avg": row[3],
            "weatherapi_accuracy_avg": row[4]
        }
        for row in rows
    ]

    # Save to JSON file
    with open("weather_data.json", "w") as json_file:
        json.dump(cities_data, json_file, indent=4)

    cursor.close()
    conn.close()
    print(" JSON file 'weather_data.json' has been updated.")

# Generate JSON when the app starts
generate_json_file()

# API to serve the JSON data
@app.route('/data', methods=['GET'])
def get_weather_data():
    with open("weather_data.json", "r") as json_file:
        data = json.load(json_file)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
