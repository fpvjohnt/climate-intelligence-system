import requests

def get_extreme_weather_data():
    print("🌪️ Extreme Weather Agent running...")
    
    # Global cities to monitor
    locations = [
        {"name": "New York, USA", "lat": 40.71, "lon": -74.01},
        {"name": "London, UK", "lat": 51.51, "lon": -0.13},
        {"name": "Tokyo, Japan", "lat": 35.68, "lon": 139.69},
        {"name": "Sydney, Australia", "lat": -33.87, "lon": 151.21},
        {"name": "Mumbai, India", "lat": 19.08, "lon": 72.88},
    ]
    
    print(f"✅ Pulling weather for {len(locations)} global cities\n")
    
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "precipitation_sum,temperature_2m_max,windspeed_10m_max",
            "timezone": "auto",
            "past_days": 7,
            "forecast_days": 1,
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "precipitation_unit": "inch"
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precip = daily.get("precipitation_sum", [])
            temp = daily.get("temperature_2m_max", [])
            
            print(f"📍 {loc['name']}")
            for i in range(len(dates)):
                print(f"  {dates[i]}: {temp[i]}°F | {precip[i]}in rain")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_extreme_weather_data()
