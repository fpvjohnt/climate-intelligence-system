import requests
from locations import US_CITIES, GLOBAL_CITIES

def get_drought_data():
    print("🏜️ Drought Monitoring Agent running...")
    print("✅ Using Open-Meteo soil moisture & precipitation deficit analysis\n")

    # US drought indicators using soil moisture + precipitation data
    print("--- US Cities ---\n")
    _analyze_drought(US_CITIES)

    print("\n--- Global Cities ---\n")
    _analyze_drought(GLOBAL_CITIES)

def _analyze_drought(locations):
    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "precipitation_sum,et0_fao_evapotranspiration",
            "hourly": "soil_moisture_0_to_1cm",
            "timezone": "auto",
            "past_days": 14,
            "forecast_days": 1,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                precip_list = daily.get("precipitation_sum", [])
                et0_list = daily.get("et0_fao_evapotranspiration", [])

                soil_vals = data.get("hourly", {}).get("soil_moisture_0_to_1cm", [])
                avg_soil = None
                if soil_vals:
                    valid = [v for v in soil_vals if v is not None]
                    avg_soil = sum(valid) / len(valid) if valid else None

                total_precip = sum(p for p in precip_list if p is not None)
                total_et0 = sum(e for e in et0_list if e is not None)

                # Drought severity based on precipitation deficit + soil moisture
                deficit = total_et0 - total_precip
                severity = "NONE"
                icon = "🟢"

                if avg_soil is not None:
                    if avg_soil < 0.05 and deficit > 30:
                        severity, icon = "EXTREME DROUGHT", "🔴"
                    elif avg_soil < 0.10 and deficit > 20:
                        severity, icon = "SEVERE DROUGHT", "🟠"
                    elif avg_soil < 0.15 and deficit > 10:
                        severity, icon = "MODERATE DROUGHT", "🟡"
                    elif deficit > 15:
                        severity, icon = "ABNORMALLY DRY", "🟡"

                soil_str = f"{avg_soil:.3f} m³/m³" if avg_soil is not None else "N/A"
                print(f"  {icon} {loc['name']}: {severity}")
                print(f"    14-day precip: {total_precip:.1f}mm | ET₀: {total_et0:.1f}mm | Deficit: {deficit:.1f}mm | Soil moisture: {soil_str}")
        except requests.RequestException:
            print(f"  ❌ {loc['name']}: request failed")

if __name__ == "__main__":
    get_drought_data()
