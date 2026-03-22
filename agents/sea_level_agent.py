import requests
from datetime import datetime, timedelta

def get_sea_level_data():
    print("🌊 Sea Level Agent running...")

    stations = [
        {"name": "San Francisco, CA", "id": "9414290"},
        {"name": "Los Angeles, CA", "id": "9410660"},
        {"name": "Seattle, WA", "id": "9447130"},
        {"name": "Galveston, TX", "id": "8771450"},
        {"name": "Key West, FL", "id": "8724580"},
        {"name": "New York (Battery), NY", "id": "8518750"},
        {"name": "Honolulu, HI", "id": "1612340"},
        {"name": "San Juan, PR", "id": "9755371"},
        {"name": "Juneau, AK", "id": "9452210"},
        {"name": "Virginia Key, FL", "id": "8723214"},
    ]

    print(f"✅ Pulling sea level data for {len(stations)} NOAA stations\n")

    end = datetime.now()
    start = end - timedelta(days=365)

    for station in stations:
        url = "https://tidesandcurrents.noaa.gov/api/datagetter"
        params = {
            "product": "monthly_mean",
            "station": station["id"],
            "datum": "MSL",
            "units": "metric",
            "time_zone": "GMT",
            "format": "json",
            "begin_date": start.strftime("%Y%m%d"),
            "end_date": end.strftime("%Y%m%d"),
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            results = data.get("data", [])
            if results:
                latest = results[-1]
                print(f"📍 {station['name']}")
                print(f"  {latest.get('year', '')}-{latest.get('month', '')}: {latest.get('MSL', 'N/A')} meters above MSL")
                print()
            else:
                error = data.get("error", {}).get("message", "No data")
                print(f"📍 {station['name']} — ⚠️ {error}\n")
        else:
            print(f"❌ Error for {station['name']}: {response.status_code}")

if __name__ == "__main__":
    get_sea_level_data()
