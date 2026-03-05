import requests
from datetime import datetime

def get_sea_level_data():
    print("🌊 Sea Level Agent running...")
    
    stations = [
        # North America
        {"name": "Los Angeles, USA", "id": "9410660"},
        {"name": "Vancouver, Canada", "id": "9443090"},
        {"name": "Galveston, Mexico Gulf", "id": "8771450"},
        # South America
        {"name": "San Juan, Puerto Rico", "id": "9755371"},
        # Pacific
        {"name": "Honolulu, Hawaii", "id": "1612340"},
        {"name": "Guam, Pacific", "id": "1630000"},
        # Asia
        {"name": "Tokyo, Japan", "id": "1619910"},
        {"name": "Mumbai, India", "id": "1617760"},
        # Australia/Pacific
        {"name": "Sydney, Australia", "id": "9751381"},
        {"name": "Auckland, New Zealand", "id": "9751401"},
    ]
    
    print(f"✅ Pulling sea level data for {len(stations)} global stations\n")
    
    for station in stations:
        url = "https://tidesandcurrents.noaa.gov/api/datagetter"
        params = {
            "product": "monthly_mean",
            "station": station["id"],
            "datum": "MSL",
            "units": "metric",
            "time_zone": "GMT",
            "format": "json",
            "begin_date": f"{datetime.now().year}0101",
            "end_date": f"{datetime.now().year}1231"
        }

        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("data", [])
            if results:
                latest = results[-1]
                month = latest.get("year", "N/A")
                height = latest.get("MSL", latest.get("highest", "N/A"))
                print(f"📍 {station['name']}")
                print(f"  {month}: {height} meters above MSL")
                print()
            else:
                error = data.get("error", {}).get("message", "No data")
                print(f"📍 {station['name']} — ⚠️ {error}\n")
        else:
            print(f"❌ Error for {station['name']}: {response.status_code}")

if __name__ == "__main__":
    get_sea_level_data()
