import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_agent(script):
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(script)),
        timeout=120
    )
    name = os.path.basename(script)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        print(f"⚠️ {name} failed (exit {result.returncode}): {stderr[:200]}")
    return name, result.stdout

def get_summary():
    print("📋 Climate Summary Agent running...")
    print("🔄 Collecting data from all agents...\n")

    agents_dir = os.path.dirname(os.path.abspath(__file__))

    agent_scripts = {
        # Core climate monitoring
        "TEMPERATURE DATA": f"{agents_dir}/temperature_agent.py",
        "EMISSIONS & AIR QUALITY": f"{agents_dir}/emissions_agent.py",
        "SEA LEVEL DATA": f"{agents_dir}/sea_level_agent.py",
        "EXTREME WEATHER": f"{agents_dir}/extreme_weather_agent.py",
        "ENERGY TRANSITION": f"{agents_dir}/energy_transition_agent.py",
        "ARCTIC CONDITIONS": f"{agents_dir}/arctic_ice_agent.py",
        "US CLIMATE": f"{agents_dir}/us_climate_agent.py",
        "GLOBAL CLIMATE": f"{agents_dir}/global_climate_agent.py",
        # Natural hazards
        "WILDFIRE RISK": f"{agents_dir}/wildfire_agent.py",
        "EARTHQUAKE ACTIVITY": f"{agents_dir}/earthquake_agent.py",
        "FLOOD & RIVER LEVELS": f"{agents_dir}/flood_river_agent.py",
        # Environmental indicators
        "SOLAR RADIATION & UV": f"{agents_dir}/solar_radiation_agent.py",
        "DROUGHT MONITORING": f"{agents_dir}/drought_agent.py",
        # Analytics
        "CLIMATE ALERTS": f"{agents_dir}/alert_system.py",
        "CLIMATE RISK SCORES": f"{agents_dir}/climate_risk_scorer.py",
    }

    results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(run_agent, path): label for label, path in agent_scripts.items()}
        for future in as_completed(futures):
            label = futures[future]
            try:
                _name, output = future.result()
                results[label] = output
            except subprocess.TimeoutExpired:
                print(f"⚠️ {label} timed out after 120s")
                results[label] = ""
            except Exception as e:
                print(f"⚠️ {label} error: {e}")
                results[label] = ""

    print("✅ All agent data collected!")
    print("🤖 Generating climate intelligence briefing...\n")
    print("=" * 60)
    print("🌍 GLOBAL CLIMATE INTELLIGENCE BRIEFING")
    print("=" * 60)

    for label in agent_scripts:
        print(f"\n{'─'*60}")
        print(f"  {label}")
        print(f"{'─'*60}")
        print(results.get(label, ""))

if __name__ == "__main__":
    get_summary()
