Weather API Accuracy App is a web-based tool designed to evaluate and compare the accuracy of multiple weather forecasting APIs. It tracks predictions and compares them against actual weather outcomes, helping users determine which API is most reliable over time.

🌟 Features
🌆 City Selector: Choose from a list of cities to view accuracy stats.

📅 3-Day Forecast Tracking: Each API provides predictions up to 3 days in advance; these are stored and later compared to real-world weather.

📊 Accuracy Grades: Calculates daily accuracy per API and overall performance averages.

☁️ Actual vs Predicted Data: Pulls actual weather data from trusted sources to grade each forecast.

🌐 Web Dashboard: Simple and clean Vue.js frontend for browsing and comparing results.

🔧 Tech Stack
Frontend: Vue.js

Backend: Python (Flask)

Database: Supabase (PostgreSQL)

APIs: Multiple weather APIs (e.g., OpenWeatherMap, WeatherAPI, etc.)

Data Sources: Scraped actual weather results

Scheduling: Daily cron job to collect predictions and update results

🔁 How It Works
Forecasts are stored daily for each API, city, and future date 3 days ahead.

Actual weather data is pulled on the relevant day and matched with previous forecasts.

Accuracy is calculated per forecast and averaged across time and APIs.

Dashboard displays stats by city and forecast day.
