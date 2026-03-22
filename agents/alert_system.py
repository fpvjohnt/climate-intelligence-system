import requests
from datetime import datetime
from locations import GLOBAL_CITIES, US_CITIES

# Thresholds based on WMO / NWS standards
ALERT_THRESHOLDS = {
    "extreme_heat": {"field": "temperature_2m_max", "op": ">=", "value": 40, "unit": "°C", "severity": "CRITICAL"},
    "heat_wave": {"field": "temperature_2m_max", "op": ">=", "value": 35, "unit": "°C", "severity": "WARNING"},
    "heavy_rain": {"field": "precipitation_sum", "op": ">=", "value": 50, "unit": "mm", "severity": "WARNING"},
    "extreme_rain": {"field": "precipitation_sum", "op": ">=", "value": 100, "unit": "mm", "severity": "CRITICAL"},
    "high_wind": {"field": "windspeed_10m_max", "op": ">=", "value": 60, "unit": "km/h", "severity": "WARNING"},
    "storm_wind": {"field": "windspeed_10m_max", "op": ">=", "value": 90, "unit": "km/h", "severity": "CRITICAL"},
    "extreme_uv": {"field": "uv_index_max", "op": ">=", "value": 11, "unit": "", "severity": "WARNING"},
    "extreme_cold": {"field": "temperature_2m_min", "op": "<=", "value": -20, "unit": "°C", "severity": "WARNING"},
}

def check_alerts():
    print("🚨 Climate Alert System running...")
    print(f"⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"✅ Checking {len(ALERT_THRESHOLDS)} alert thresholds across all locations\n")

    all_locations = US_CITIES + GLOBAL_CITIES
    seen = set()
    locations = []
    for loc in all_locations:
        if loc["name"] not in seen:
            seen.add(loc["name"])
            locations.append(loc)

    alerts = []

    for loc in locations:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,uv_index_max",
            "timezone": "auto",
            "forecast_days": 3,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                continue

            data = response.json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])

            for day_idx, date in enumerate(dates):
                for alert_name, threshold in ALERT_THRESHOLDS.items():
                    values = daily.get(threshold["field"], [])
                    if day_idx >= len(values):
                        continue
                    val = values[day_idx]
                    if val is None:
                        continue

                    triggered = False
                    if threshold["op"] == ">=" and val >= threshold["value"]:
                        triggered = True
                    elif threshold["op"] == "<=" and val <= threshold["value"]:
                        triggered = True

                    if triggered:
                        alert = {
                            "location": loc["name"],
                            "date": date,
                            "alert": alert_name,
                            "severity": threshold["severity"],
                            "value": val,
                            "threshold": threshold["value"],
                            "unit": threshold["unit"],
                        }
                        alerts.append(alert)
        except requests.RequestException:
            pass

    # Print alerts grouped by severity
    critical = [a for a in alerts if a["severity"] == "CRITICAL"]
    warnings = [a for a in alerts if a["severity"] == "WARNING"]

    if critical:
        print(f"🔴 CRITICAL ALERTS ({len(critical)}):")
        print("-" * 50)
        for a in critical:
            print(f"  🔴 {a['location']} ({a['date']}): {a['alert'].replace('_', ' ').upper()}")
            print(f"     Value: {a['value']}{a['unit']} (threshold: {a['threshold']}{a['unit']})")
        print()

    if warnings:
        print(f"🟠 WARNINGS ({len(warnings)}):")
        print("-" * 50)
        for a in warnings:
            print(f"  🟠 {a['location']} ({a['date']}): {a['alert'].replace('_', ' ').upper()}")
            print(f"     Value: {a['value']}{a['unit']} (threshold: {a['threshold']}{a['unit']})")
        print()

    if not alerts:
        print("✅ No alerts triggered across all monitored locations.\n")

    print(f"📊 Summary: {len(critical)} critical, {len(warnings)} warnings across {len(locations)} locations")

    return alerts

if __name__ == "__main__":
    check_alerts()
