from utils.api_client import get_weather
import pandas as pd
from datetime import datetime, timedelta

cities = ["New York", "London", "Mumbai", "Tokyo", "Sydney", "Paris", "Toronto", "Cape Town", "Dubai", "Singapore"]
start_date = "2025-05-01"
today = datetime.today().strftime('%Y-%m-%d')

forecast_data = []
actual_data = []

for city in cities:
    data = get_weather(city, start_date)
    if data:
        day = data['forecast']['forecastday'][0]['day']
        forecast_data.append({
            "City": city,
            "Date": start_date,
            "Temp": day['avgtemp_c'],
            "Humidity": day['avghumidity'],
            "Condition": day['condition']['text']
        })

current = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(today, "%Y-%m-%d")

while current <= end:
    date_str = current.strftime('%Y-%m-%d')
    for city in cities:
        data = get_weather(city, date_str)
        if data:
            day = data['forecast']['forecastday'][0]['day']
            actual_data.append({
                "City": city,
                "Date": date_str,
                "Temp": day['avgtemp_c'],
                "Humidity": day['avghumidity'],
                "Condition": day['condition']['text']
            })
    current += timedelta(days=1)

df_forecast = pd.DataFrame(forecast_data)
df_actual = pd.DataFrame(actual_data)

print("Forecast DataFrame:")
print(df_forecast.head(10))
print("Actual DataFrame:")
print(df_actual.head(10))
# Save the forecast and actual data to CSV files


from datetime import datetime
start_date = datetime.today().strftime('%Y-%m-%d')


df_merged = df_actual.merge(df_forecast, on="City", suffixes=("_Actual", "_Forecast"))
df_merged["Temp_Diff"] = df_merged["Temp_Actual"] - df_merged["Temp_Forecast"]
df_merged["Humidity_Diff"] = df_merged["Humidity_Actual"] - df_merged["Humidity_Forecast"]
df_merged["Condition_Match"] = df_merged["Condition_Actual"] == df_merged["Condition_Forecast"]

df_merged.to_csv("output/weather_report.csv", index=False)
print("✅ Report generated at: output/weather_report.csv")
