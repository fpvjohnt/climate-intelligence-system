import requests
import os
from locations import GLOBAL_CITIES

def get_wildfire_data(map_key=None):
    print("🔥 Wildfire Agent running...")

    if map_key:
        print("✅ Using NASA FIRMS satellite fire detection\n")
        # NASA FIRMS API - active fire hotspots by region
        regions = [
            {"name": "Western US", "bbox": "-125,32,-100,49"},
            {"name": "Amazon Basin", "bbox": "-75,-20,-45,5"},
            {"name": "Central Africa", "bbox": "10,-10,35,10"},
            {"name": "Southeast Asia", "bbox": "95,0,130,25"},
            {"name": "Southern Europe / Mediterranean", "bbox": "-10,35,35,47"},
            {"name": "Australia", "bbox": "110,-45,155,-10"},
        ]

        for region in regions:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{map_key}/VIIRS_NOAA20_NRT/{region['bbox']}/2"
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    lines = response.text.strip().split("\n")
                    fire_count = max(0, len(lines) - 1)  # subtract header
                    print(f"📍 {region['name']}: {fire_count} active fire detections (last 48h)")
                else:
                    print(f"⚠️ {region['name']}: API returned {response.status_code}")
            except requests.RequestException as e:
                print(f"❌ {region['name']}: {e}")
        print()
    else:
        print("⚠️ No NASA FIRMS MAP_KEY — using Open-Meteo weather risk indicators\n")

    # Always show fire weather risk using Open-Meteo (high temp + low humidity + high wind)
    print("🌡️ Fire Weather Risk Index (temp + humidity + wind):\n")
    for loc in GLOBAL_CITIES:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "temperature_2m_max,precipitation_sum,windspeed_10m_max",
            "hourly": "relativehumidity_2m",
            "timezone": "auto",
            "forecast_days": 1,
        }
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                temp = (daily.get("temperature_2m_max", [None]) or [None])[0]
                wind = (daily.get("windspeed_10m_max", [None]) or [None])[0]
                precip = (daily.get("precipitation_sum", [None]) or [None])[0]
                humidity_vals = data.get("hourly", {}).get("relativehumidity_2m", [])
                avg_humidity = sum(humidity_vals) / len(humidity_vals) if humidity_vals else None

                if temp is not None and wind is not None and avg_humidity is not None:
                    # Simple fire weather index: high temp + low humidity + high wind = danger
                    risk = 0
                    if temp > 35: risk += 3
                    elif temp > 30: risk += 2
                    elif temp > 25: risk += 1
                    if avg_humidity < 20: risk += 3
                    elif avg_humidity < 30: risk += 2
                    elif avg_humidity < 40: risk += 1
                    if wind > 40: risk += 3
                    elif wind > 25: risk += 2
                    elif wind > 15: risk += 1
                    if precip and precip > 5: risk = max(0, risk - 2)

                    labels = {0: "LOW", 1: "LOW", 2: "LOW", 3: "MODERATE",
                              4: "MODERATE", 5: "HIGH", 6: "HIGH",
                              7: "VERY HIGH", 8: "EXTREME", 9: "EXTREME"}
                    label = labels.get(risk, "EXTREME")
                    icon = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🟠",
                            "VERY HIGH": "🔴", "EXTREME": "🔴"}.get(label, "⚪")

                    print(f"  {icon} {loc['name']}: {label} (temp={temp}°C, humidity={avg_humidity:.0f}%, wind={wind}km/h)")
        except requests.RequestException:
            pass

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../config/.env")
    map_key = os.getenv("NASA_FIRMS_MAP_KEY")
    get_wildfire_data(map_key)
