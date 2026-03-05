import requests
import os


def get_energy_transition_data(api_key):
    print("⚡ Energy Transition Agent running...")

    url = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"

    params = {
        "api_key": api_key,
        "frequency": "annual",
        "data[0]": "generation",
        "facets[fueltypeid][]": ["SUN", "WND", "HYC", "NUC", "COL", "NG"],
        "facets[location][]": "US",
        "facets[sectorid][]": "99",
        "start": "2018",
        "end": "2023",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": 50
    }

    response = requests.get(url, params=params, timeout=15)

    results = []
    if response.status_code == 200:
        data = response.json()
        records = data.get("response", {}).get("data", [])
        if records:
            print(f"✅ Got {len(records)} energy records\n")

            # Group by fuel type
            fuel_map = {
                "SUN": "Solar",
                "WND": "Wind",
                "HYC": "Hydro",
                "NUC": "Nuclear",
                "COL": "Coal",
                "NG": "Natural Gas"
            }

            fuel_icons = {
                "SUN": "☀️", "WND": "💨", "HYC": "💧",
                "NUC": "⚛️", "COL": "🏭", "NG": "🔥"
            }

            by_fuel = {}
            for r in records:
                fuel = r.get("fueltypeid", "Unknown")
                year = r.get("period", "")
                gen = r.get("generation", 0)
                if fuel not in by_fuel:
                    by_fuel[fuel] = []
                by_fuel[fuel].append((year, gen))
                results.append({
                    "fuel": fuel_map.get(fuel, fuel),
                    "fuel_id": fuel,
                    "year": year,
                    "generation": float(gen or 0),
                })

            for fuel, recs in by_fuel.items():
                label = f"{fuel_icons.get(fuel, '')} {fuel_map.get(fuel, fuel)}"
                print(f"{label}")
                for year, gen in recs[:3]:
                    print(f"  {year}: {round(float(gen or 0), 1)} thousand MWh")
                print()
        else:
            print(f"⚠️ No data: {data}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text[:200]}")

    return results


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../config/.env")
    api_key = os.getenv("EIA_API_KEY")
    get_energy_transition_data(api_key)
