import requests
from locations import GLOBAL_CITIES

def get_solar_radiation_data():
    print("☀️ Solar Radiation & UV Agent running...")
    print("✅ Using Open-Meteo Solar & UV API\n")

    for loc in GLOBAL_CITIES:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "uv_index_max,uv_index_clear_sky_max,shortwave_radiation_sum,sunshine_duration",
            "timezone": "auto",
            "forecast_days": 1,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                uv_max = (daily.get("uv_index_max", [None]) or [None])[0]
                uv_clear = (daily.get("uv_index_clear_sky_max", [None]) or [None])[0]
                radiation = (daily.get("shortwave_radiation_sum", [None]) or [None])[0]
                sunshine = (daily.get("sunshine_duration", [None]) or [None])[0]

                uv_label = "LOW"
                uv_icon = "🟢"
                if uv_max is not None:
                    if uv_max >= 11:
                        uv_label, uv_icon = "EXTREME", "🟣"
                    elif uv_max >= 8:
                        uv_label, uv_icon = "VERY HIGH", "🔴"
                    elif uv_max >= 6:
                        uv_label, uv_icon = "HIGH", "🟠"
                    elif uv_max >= 3:
                        uv_label, uv_icon = "MODERATE", "🟡"

                sunshine_hrs = f"{sunshine / 3600:.1f}h" if sunshine else "N/A"
                radiation_str = f"{radiation:.1f} MJ/m²" if radiation else "N/A"

                print(f"  📍 {loc['name']}")
                print(f"    {uv_icon} UV Index: {uv_max} ({uv_label}) | Clear-sky UV: {uv_clear}")
                print(f"    ☀️ Solar Radiation: {radiation_str} | Sunshine: {sunshine_hrs}")
        except requests.RequestException:
            print(f"  ❌ {loc['name']}: request failed")
    print()

if __name__ == "__main__":
    get_solar_radiation_data()
