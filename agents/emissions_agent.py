import requests
from locations import GLOBAL_CITIES

def get_emissions_data():
    print("💨 Emissions Agent running...")

    locations = GLOBAL_CITIES
    
    print(f"✅ Pulling air quality & emissions for {len(locations)} global cities\n")
    
    for loc in locations:
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "hourly": "carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,pm2_5",
            "timezone": "auto",
            "past_days": 1,
            "forecast_days": 1
        }
        
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            hourly = data.get("hourly", {})
            co = hourly.get("carbon_monoxide", [None])[0]
            no2 = hourly.get("nitrogen_dioxide", [None])[0]
            so2 = hourly.get("sulphur_dioxide", [None])[0]
            pm25 = hourly.get("pm2_5", [None])[0]
            
            print(f"📍 {loc['name']}")
            print(f"  CO: {co} μg/m³ | NO2: {no2} μg/m³ | SO2: {so2} μg/m³ | PM2.5: {pm25} μg/m³")
            print()
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

if __name__ == "__main__":
    get_emissions_data()
