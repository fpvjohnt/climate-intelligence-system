import requests
from datetime import datetime, timedelta

def get_flood_river_data():
    print("🌊 Flood & River Level Agent running...")
    print("✅ Using USGS Water Services API\n")

    # Major US river monitoring stations
    stations = [
        {"name": "Mississippi River at Memphis, TN", "id": "07032000"},
        {"name": "Mississippi River at St. Louis, MO", "id": "07010000"},
        {"name": "Colorado River at Austin, TX", "id": "08158000"},
        {"name": "Columbia River at The Dalles, OR", "id": "14105700"},
        {"name": "Missouri River at Omaha, NE", "id": "06610000"},
        {"name": "Ohio River at Louisville, KY", "id": "03294500"},
        {"name": "Sacramento River at Sacramento, CA", "id": "11447650"},
        {"name": "Hudson River at Green Island, NY", "id": "01358000"},
        {"name": "Rio Grande at El Paso, TX", "id": "08364000"},
        {"name": "Potomac River at Washington, DC", "id": "01646500"},
    ]

    print(f"📊 Monitoring {len(stations)} major US river stations\n")

    for station in stations:
        url = "https://waterservices.usgs.gov/nwis/iv/"
        params = {
            "format": "json",
            "sites": station["id"],
            "parameterCd": "00065,00060",  # gage height + discharge
            "period": "P1D",  # last 24 hours
            "siteStatus": "active",
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                time_series = data.get("value", {}).get("timeSeries", [])

                gage_height = None
                discharge = None

                for ts in time_series:
                    var_code = ts.get("variable", {}).get("variableCode", [{}])[0].get("value", "")
                    values = ts.get("values", [{}])[0].get("value", [])
                    if values:
                        latest = values[-1]
                        val = latest.get("value", "N/A")
                        if var_code == "00065":
                            gage_height = val
                        elif var_code == "00060":
                            discharge = val

                parts = [f"📍 {station['name']}"]
                details = []
                if gage_height and gage_height != "-999999":
                    height_ft = float(gage_height)
                    details.append(f"Gage Height: {height_ft:.2f} ft")
                    # Flag high water levels
                    if height_ft > 30:
                        details.append("🔴 FLOOD STAGE")
                    elif height_ft > 20:
                        details.append("🟠 HIGH")
                if discharge and discharge != "-999999":
                    details.append(f"Discharge: {float(discharge):,.0f} ft³/s")

                if details:
                    print(f"  {parts[0]}")
                    print(f"    {' | '.join(details)}")
                else:
                    print(f"  {parts[0]} — ⚠️ No recent data")
            else:
                print(f"  ⚠️ {station['name']}: HTTP {response.status_code}")
        except requests.RequestException as e:
            print(f"  ❌ {station['name']}: {e}")

if __name__ == "__main__":
    get_flood_river_data()
