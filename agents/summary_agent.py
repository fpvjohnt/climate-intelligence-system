import subprocess
import sys
import os

def run_agent(script):
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(script))
    )
    return result.stdout

def get_summary():
    print("📋 Climate Summary Agent running...")
    print("🔄 Collecting data from all agents...\n")
    
    agents_dir = os.path.dirname(os.path.abspath(__file__))
    
    temperature  = run_agent(f"{agents_dir}/temperature_agent.py")
    emissions    = run_agent(f"{agents_dir}/emissions_agent.py")
    sea_level    = run_agent(f"{agents_dir}/sea_level_agent.py")
    weather      = run_agent(f"{agents_dir}/extreme_weather_agent.py")
    energy       = run_agent(f"{agents_dir}/energy_transition_agent.py")
    arctic       = run_agent(f"{agents_dir}/arctic_ice_agent.py")
    us_climate   = run_agent(f"{agents_dir}/us_climate_agent.py")
    global_climate = run_agent(f"{agents_dir}/global_climate_agent.py")
    
    combined = f"""
TEMPERATURE DATA:
{temperature}

EMISSIONS & AIR QUALITY:
{emissions}

SEA LEVEL DATA:
{sea_level}

EXTREME WEATHER:
{weather}

ENERGY TRANSITION:
{energy}

ARCTIC CONDITIONS:
{arctic}

US CLIMATE:
{us_climate}

GLOBAL CLIMATE:
{global_climate}
"""
    
    print("✅ All agent data collected!")
    print("🤖 Generating AI summary...\n")
    print("=" * 60)
    print("🌍 GLOBAL CLIMATE INTELLIGENCE BRIEFING")
    print("=" * 60)
    print(combined)

if __name__ == "__main__":
    get_summary()
