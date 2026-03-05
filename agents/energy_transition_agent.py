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
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("response", {}).get("data", [])
        if results:
            print(f"✅ Got {len(results)} energy records\n")
            
            # Group by fuel type
            fuel_map = {
                "SUN": "☀️ Solar",
                "WND": "💨 Wind",
                "HYC": "💧 Hydro",
                "NUC": "⚛️ Nuclear",
                "COL": "🏭 Coal",
                "NG": "🔥 Natural Gas"
            }
            
            by_fuel = {}
            for r in results:
                fuel = r.get("fueltypeid", "Unknown")
                year = r.get("period", "")
                gen = r.get("generation", 0)
                if fuel not in by_fuel:
                    by_fuel[fuel] = []
                by_fuel[fuel].append((year, gen))
            
            for fuel, records in by_fuel.items():
                label = fuel_map.get(fuel, fuel)
                print(f"{label}")
                for year, gen in records[:3]:
                    print(f"  {year}: {round(float(gen or 0), 1)} thousand MWh")
                print()
        else:
            print(f"⚠️ No data: {data}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text[:200]}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv("../config/.env")
    api_key = os.getenv("EIA_API_KEY")
    get_energy_transition_data(api_key)
