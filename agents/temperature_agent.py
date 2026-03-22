import requests
from locations import GLOBAL_CITIES

def get_temperature_data():
    print("🌡️ Temperature Agent running...")

    locations = GLOBAL_CITIES
    
    print(f"✅ Pulling temperatures for {len(locations)} global cities\n")
    
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto",
            "past_days": 1,
            "forecast_days": 1,
            "temperature_unit": "fahrenheit"
        }
        
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            
            print(f"📍 {loc['name']}")
            for i in range(len(dates)):
                print(f"  {dates[i]}: High {temp_max[i]}°F | Low {temp_min[i]}°F")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_temperature_data()
