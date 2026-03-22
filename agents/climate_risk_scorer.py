import requests
import json
from locations import GLOBAL_CITIES, US_CITIES

# Risk thresholds inspired by industry standards (TCFD, Jupiter Intelligence, ClimateAI)
RISK_WEIGHTS = {
    "heat": 0.20,
    "precipitation": 0.15,
    "wind": 0.15,
    "air_quality": 0.15,
    "drought": 0.15,
    "uv": 0.10,
    "humidity": 0.10,
}

def _score_heat(temp_max_c):
    if temp_max_c is None: return 0
    if temp_max_c >= 45: return 10
    if temp_max_c >= 40: return 8
    if temp_max_c >= 35: return 6
    if temp_max_c >= 30: return 4
    if temp_max_c >= 25: return 2
    return 0

def _score_precipitation(precip_mm):
    if precip_mm is None: return 0
    if precip_mm >= 100: return 10
    if precip_mm >= 50: return 8
    if precip_mm >= 25: return 6
    if precip_mm >= 10: return 3
    return 0

def _score_wind(wind_kmh):
    if wind_kmh is None: return 0
    if wind_kmh >= 100: return 10
    if wind_kmh >= 75: return 8
    if wind_kmh >= 50: return 6
    if wind_kmh >= 30: return 3
    return 0

def _score_air_quality(pm25):
    if pm25 is None: return 0
    if pm25 >= 150: return 10
    if pm25 >= 75: return 8
    if pm25 >= 50: return 6
    if pm25 >= 25: return 3
    if pm25 >= 12: return 1
    return 0

def _score_drought(soil_moisture, precip_14d):
    if soil_moisture is None: return 0
    if soil_moisture < 0.05 and precip_14d < 5: return 10
    if soil_moisture < 0.10 and precip_14d < 10: return 7
    if soil_moisture < 0.15: return 4
    return 0

def _score_uv(uv_index):
    if uv_index is None: return 0
    if uv_index >= 11: return 10
    if uv_index >= 8: return 7
    if uv_index >= 6: return 4
    if uv_index >= 3: return 2
    return 0

def _score_humidity(humidity_pct):
    if humidity_pct is None: return 0
    # Both extremes are risky
    if humidity_pct < 15 or humidity_pct > 95: return 8
    if humidity_pct < 20 or humidity_pct > 90: return 5
    if humidity_pct < 30 or humidity_pct > 85: return 3
    return 0

def _risk_label(score):
    if score >= 8: return "CRITICAL", "🔴"
    if score >= 6: return "HIGH", "🟠"
    if score >= 4: return "MODERATE", "🟡"
    if score >= 2: return "LOW", "🟢"
    return "MINIMAL", "⚪"

def compute_risk_scores():
    print("📊 Climate Risk Scoring Engine running...")
    print("✅ Computing multi-hazard risk scores for all locations\n")

    all_locations = US_CITIES + GLOBAL_CITIES
    # Deduplicate by name
    seen = set()
    locations = []
    for loc in all_locations:
        if loc["name"] not in seen:
            seen.add(loc["name"])
            locations.append(loc)

    results = []

    for loc in locations:
        try:
            # Fetch weather data
            weather_resp = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": loc["lat"], "longitude": loc["lon"],
                "daily": "temperature_2m_max,precipitation_sum,windspeed_10m_max,uv_index_max,et0_fao_evapotranspiration",
                "hourly": "relativehumidity_2m,soil_moisture_0_to_1cm",
                "timezone": "auto", "past_days": 14, "forecast_days": 1,
            }, timeout=30)

            # Fetch air quality
            aq_resp = requests.get("https://air-quality-api.open-meteo.com/v1/air-quality", params={
                "latitude": loc["lat"], "longitude": loc["lon"],
                "hourly": "pm2_5", "timezone": "auto", "forecast_days": 1,
            }, timeout=30)

            if weather_resp.status_code != 200:
                continue

            w = weather_resp.json()
            daily = w.get("daily", {})
            hourly = w.get("hourly", {})

            # Today's values (last entry since we have past_days)
            temp_max_all = daily.get("temperature_2m_max", [])
            precip_all = daily.get("precipitation_sum", [])
            wind_all = daily.get("windspeed_10m_max", [])
            uv_all = daily.get("uv_index_max", [])

            temp_max = temp_max_all[-1] if temp_max_all else None
            precip_today = precip_all[-1] if precip_all else None
            wind_max = wind_all[-1] if wind_all else None
            uv_max = uv_all[-1] if uv_all else None

            # 14-day precipitation total
            precip_14d = sum(p for p in precip_all if p is not None)

            # Humidity average (today's hours only)
            hum_vals = hourly.get("relativehumidity_2m", [])
            today_hum = hum_vals[-24:] if len(hum_vals) >= 24 else hum_vals
            avg_humidity = sum(h for h in today_hum if h) / max(len([h for h in today_hum if h]), 1)

            # Soil moisture average
            soil_vals = hourly.get("soil_moisture_0_to_1cm", [])
            valid_soil = [s for s in soil_vals if s is not None]
            avg_soil = sum(valid_soil) / len(valid_soil) if valid_soil else None

            # Air quality
            pm25 = None
            if aq_resp.status_code == 200:
                aq = aq_resp.json()
                pm_vals = aq.get("hourly", {}).get("pm2_5", [])
                valid_pm = [p for p in pm_vals if p is not None]
                pm25 = sum(valid_pm) / len(valid_pm) if valid_pm else None

            # Compute individual scores
            scores = {
                "heat": _score_heat(temp_max),
                "precipitation": _score_precipitation(precip_today),
                "wind": _score_wind(wind_max),
                "air_quality": _score_air_quality(pm25),
                "drought": _score_drought(avg_soil, precip_14d),
                "uv": _score_uv(uv_max),
                "humidity": _score_humidity(avg_humidity),
            }

            # Weighted composite score
            composite = sum(scores[k] * RISK_WEIGHTS[k] for k in scores)
            label, icon = _risk_label(composite)

            result = {
                "location": loc["name"],
                "lat": loc["lat"],
                "lon": loc["lon"],
                "composite_score": round(composite, 2),
                "risk_level": label,
                "scores": scores,
                "raw": {
                    "temp_max_c": temp_max,
                    "precip_today_mm": precip_today,
                    "precip_14d_mm": round(precip_14d, 1),
                    "wind_max_kmh": wind_max,
                    "uv_index": uv_max,
                    "humidity_pct": round(avg_humidity, 1),
                    "soil_moisture": round(avg_soil, 4) if avg_soil else None,
                    "pm25": round(pm25, 1) if pm25 else None,
                },
            }
            results.append(result)

            # Top hazards for this location
            top_hazards = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top = [f"{k}={v}" for k, v in top_hazards if v >= 3]

            print(f"  {icon} {loc['name']}: {composite:.1f}/10 ({label})")
            if top:
                print(f"    Top hazards: {', '.join(top)}")

        except requests.RequestException:
            print(f"  ❌ {loc['name']}: request failed")

    # Print ranking
    results.sort(key=lambda x: x["composite_score"], reverse=True)
    print(f"\n{'='*50}")
    print("🏆 RISK RANKING (highest to lowest)")
    print(f"{'='*50}")
    for i, r in enumerate(results[:10], 1):
        label, icon = _risk_label(r["composite_score"])
        print(f"  {i}. {icon} {r['location']}: {r['composite_score']:.1f}/10 ({label})")

    return results

if __name__ == "__main__":
    compute_risk_scores()
