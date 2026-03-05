import requests


def get_emissions_data():
    print("💨 Emissions Agent running...")

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

    print(f"✅ Pulling air quality & emissions for {len(locations)} global cities\n")

    results = []
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

        response = requests.get(url, params=params, timeout=15)

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

            results.append({
                "city": loc["name"],
                "co": co,
                "no2": no2,
                "so2": so2,
                "pm25": pm25,
            })
        else:
            print(f"❌ Error for {loc['name']}: {response.status_code}")

    return results


if __name__ == "__main__":
    get_emissions_data()
