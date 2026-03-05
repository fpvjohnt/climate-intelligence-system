import requests

def get_arctic_ice_data():
    print("🧊 Arctic Ice Agent running...")
    
    # NSIDC public data - current sea ice extent
    url = "https://nsidc.org/api/seaice/v2/extent"
    
    # Use open-meteo for real-time arctic conditions instead
    locations = [
        {"name": "Arctic Ocean", "lat": 85.0, "lon": 0.0},
        {"name": "Greenland", "lat": 72.0, "lon": -40.0},
        {"name": "Alaska Arctic", "lat": 71.0, "lon": -156.0},
        {"name": "Siberia Arctic", "lat": 73.0, "lon": 120.0},
        {"name": "Canadian Arctic", "lat": 75.0, "lon": -95.0},
        {"name": "Antarctic Peninsula", "lat": -65.0, "lon": -64.0},
    ]
    
    print(f"✅ Pulling arctic conditions for {len(locations)} polar regions\n")
    
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,snowfall_sum,precipitation_sum",
            "timezone": "auto",
            "past_days": 3,
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
            snowfall = daily.get("snowfall_sum", [])
            
            print(f"📍 {loc['name']}")
            for i in range(len(dates)):
                print(f"  {dates[i]}: High {temp_max[i]}°F | Low {temp_min[i]}°F | Snow {snowfall[i]}mm")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_arctic_ice_data()
