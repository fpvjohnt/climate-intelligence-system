import os
from dotenv import load_dotenv

# Load API keys
load_dotenv("config/.env")

NOAA_KEY = os.getenv("NOAA_API_KEY")
EIA_KEY = os.getenv("EIA_API_KEY")
NASA_TOKEN = os.getenv("NASA_EARTHDATA_TOKEN")

print("Climate Intelligence System starting...")
print(f"NOAA key loaded: {'✅' if NOAA_KEY else '❌'}")
print(f"EIA key loaded: {'✅' if EIA_KEY else '❌'}")
print(f"NASA key loaded: {'✅' if NASA_TOKEN else '❌'}")
