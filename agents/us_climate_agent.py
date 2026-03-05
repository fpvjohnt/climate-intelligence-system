import requests

def get_us_climate_data():
    print("🇺🇸 US Climate Agent running...")
    
    locations = [
        {"name": "Los Angeles, CA", "lat": 34.05, "lon": -118.24},
        {"name": "San Francisco, CA", "lat": 37.77, "lon": -122.41},
        {"name": "New York, NY", "lat": 40.71, "lon": -74.01},
        {"name": "Miami, FL", "lat": 25.77, "lon": -80.19},
        {"name": "Chicago, IL", "lat": 41.88, "lon": -87.63},
        {"name": "Houston, TX", "lat": 29.76, "lon": -95.37},
        {"name": "Phoenix, AZ", "lat": 33.45, "lon": -112.07},
        {"name": "Seattle, WA", "lat": 47.61, "lon": -122.33},
        {"name": "Denver, CO", "lat": 39.74, "lon": -104.98},
        {"name": "New Orleans, LA", "lat": 29.95, "lon": -90.07},
    ]
    
    print(f"✅ Pulling climate data for {len(locations)} US cities\n")
    
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
            "timezone": "auto",
            "past_days": 1,
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
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            precip = daily.get("precipitation_sum", [])
            wind = daily.get("windspeed_10m_max", [])
            
            print(f"📍 {loc['name']}")
            for i in range(len(dates)):
                print(f"  {dates[i]}: High {temp_max[i]}°F | Low {temp_min[i]}°F | Rain {precip[i]}in | Wind {wind[i]}mph")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_us_climate_data()
