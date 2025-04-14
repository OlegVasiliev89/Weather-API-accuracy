The Weather API Accuracy Checker is a full-stack Python + Vue.js system designed to determine which weather API is most accurate in different parts of the world. 
It helps users and developers understand which forecast service (OpenWeather, WeatherBit, or WeatherAPI) provides the most reliable data for their specific city.
Every day, the app.py script records 3-day-ahead forecasts from three different weather APIs for each city. It stores these predictions in a PostgreSQL (Supabase) database.
The weather_checker.py script runs every 30 minutes to check if it's 12:00 PM local time in any city. When it is, it scrapes the actual observed temperature from a reliable web source and stores it in the database.
The difference between the forecasted and actual temperature is calculated as API accuracy for each city and stored.
Vue.js (App.vue) fetches the latest average errors from a JSON file served by supa_back.py.
It lets users select a city and instantly see how accurate each API has been, based on the previous day’s forecasts.
