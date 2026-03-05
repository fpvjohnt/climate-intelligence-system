import requests

def get_temperature_data():
    print("🌡️ Temperature Agent running...")
    
    locations = [
        # North America
        {"name": "Los Angeles, USA", "lat": 34.05, "lon": -118.24},
        {"name": "Toronto, Canada", "lat": 43.65, "lon": -79.38},
        {"name": "Mexico City, Mexico", "lat": 19.43, "lon": -99.13},
        # South America
        {"name": "São Paulo, Brazil", "lat": -23.55, "lon": -46.63},
        {"name": "Buenos Aires, Argentina", "lat": -34.60, "lon": -58.38},
        # Europe
        {"name": "London, UK", "lat": 51.51, "lon": -0.13},
        {"name": "Berlin, Germany", "lat": 52.52, "lon": 13.40},
        # Middle East
        {"name": "Dubai, UAE", "lat": 25.20, "lon": 55.27},
        {"name": "Riyadh, Saudi Arabia", "lat": 24.69, "lon": 46.72},
        # Asia
        {"name": "Tokyo, Japan", "lat": 35.68, "lon": 139.69},
        {"name": "Beijing, China", "lat": 39.90, "lon": 116.40},
        {"name": "Mumbai, India", "lat": 19.08, "lon": 72.88},
        # Australia/Pacific
        {"name": "Sydney, Australia", "lat": -33.87, "lon": 151.21},
        {"name": "Auckland, New Zealand", "lat": -36.85, "lon": 174.76},
    ]
    
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
        
        response = requests.get(url, params=params)
        
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
