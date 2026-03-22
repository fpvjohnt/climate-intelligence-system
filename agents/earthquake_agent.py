import requests
from datetime import datetime, timedelta

def get_earthquake_data():
    print("🌋 Earthquake & Seismic Agent running...")
    print("✅ Using USGS Earthquake Hazards API\n")

    # Significant earthquakes in the last 7 days
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    end = datetime.utcnow()
    start = end - timedelta(days=7)

    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": 4.0,
        "orderby": "magnitude",
        "limit": 20,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            meta = data.get("metadata", {})
            print(f"📊 {meta.get('count', 0)} earthquakes M4.0+ in the last 7 days\n")

            for quake in features:
                props = quake.get("properties", {})
                geo = quake.get("geometry", {}).get("coordinates", [])
                mag = props.get("mag", "?")
                place = props.get("place", "Unknown")
                time_ms = props.get("time", 0)
                tsunami = props.get("tsunami", 0)
                alert = props.get("alert")

                quake_time = datetime.utcfromtimestamp(time_ms / 1000).strftime("%Y-%m-%d %H:%M UTC")

                icon = "🟢"
                if mag >= 7: icon = "🔴"
                elif mag >= 6: icon = "🟠"
                elif mag >= 5: icon = "🟡"

                line = f"  {icon} M{mag} — {place} ({quake_time})"
                if tsunami: line += " 🌊 TSUNAMI WARNING"
                if alert: line += f" [alert: {alert}]"
                print(line)

            # Summary stats
            if features:
                mags = [f["properties"]["mag"] for f in features if f["properties"].get("mag")]
                print(f"\n📈 Stats: max M{max(mags)}, avg M{sum(mags)/len(mags):.1f}, count={len(mags)}")
        else:
            print(f"❌ USGS API error: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")

    # Also check for significant recent quakes (last 24h, any magnitude 5+)
    print("\n--- Last 24h M5.0+ ---")
    params_24h = {
        "format": "geojson",
        "starttime": (end - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": 5.0,
        "orderby": "time",
    }
    try:
        response = requests.get(url, params=params_24h, timeout=30)
        if response.status_code == 200:
            data = response.json()
            features = data.get("features", [])
            if features:
                for quake in features:
                    props = quake.get("properties", {})
                    mag = props.get("mag", "?")
                    place = props.get("place", "Unknown")
                    print(f"  ⚡ M{mag} — {place}")
            else:
                print("  ✅ No M5.0+ earthquakes in the last 24 hours")
    except requests.RequestException:
        print("  ⚠️ Could not fetch 24h data")

if __name__ == "__main__":
    get_earthquake_data()
