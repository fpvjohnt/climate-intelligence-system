import requests
from locations import EXTREME_WEATHER_CITIES

def get_extreme_weather_data():
    print("🌪️ Extreme Weather Agent running...")

    locations = EXTREME_WEATHER_CITIES
    
    print(f"✅ Pulling weather for {len(locations)} global cities\n")
    
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "precipitation_sum,temperature_2m_max,windspeed_10m_max,weathercode",
            "timezone": "auto",
            "past_days": 7,
            "forecast_days": 1
        }
        
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precip = daily.get("precipitation_sum", [])
            temp = daily.get("temperature_2m_max", [])
            wind = daily.get("windspeed_10m_max", [])

            print(f"📍 {loc['name']}")
            for i in range(len(dates)):
                print(f"  {dates[i]}: {temp[i]}°C | {precip[i]} mm rain | Wind {wind[i]} km/h")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_extreme_weather_data()
