import requests
from locations import EXTENDED_GLOBAL_CITIES

def get_global_climate_data():
    print("🌍 Global Climate Agent running...")

    regions = EXTENDED_GLOBAL_CITIES
    
    print(f"✅ Pulling global climate data for {len(regions)} regions\n")
    
    for loc in regions:
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
        
        response = requests.get(url, params=params, timeout=30)

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
    get_global_climate_data()
