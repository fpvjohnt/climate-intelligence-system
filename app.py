import sys
import os
import io
import threading
from flask import Flask, render_template, jsonify

# Add project root to path so agents can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv("config/.env")

from agents.temperature_agent import get_temperature_data
from agents.emissions_agent import get_emissions_data
from agents.global_climate_agent import get_global_climate_data
from agents.extreme_weather_agent import get_extreme_weather_data
from agents.arctic_ice_agent import get_arctic_ice_data
from agents.sea_level_agent import get_sea_level_data
from agents.us_climate_agent import get_us_climate_data
from agents.energy_transition_agent import get_energy_transition_data
from agents.summary_agent import get_summary

app = Flask(__name__)

# Registry of all available agents
AGENTS = {
    "temperature": {
        "name": "Temperature Agent",
        "icon": "🌡️",
        "description": "Current temperatures for 14 global cities",
        "color": "#e74c3c",
        "func": get_temperature_data,
    },
    "emissions": {
        "name": "Emissions & Air Quality",
        "icon": "💨",
        "description": "CO, NO2, SO2, PM2.5 levels for 14 global cities",
        "color": "#95a5a6",
        "func": get_emissions_data,
    },
    "global_climate": {
        "name": "Global Climate",
        "icon": "🌍",
        "description": "Weather data across 18 global regions",
        "color": "#27ae60",
        "func": get_global_climate_data,
    },
    "extreme_weather": {
        "name": "Extreme Weather",
        "icon": "🌪️",
        "description": "7-day precipitation & wind for 5 major cities",
        "color": "#8e44ad",
        "func": get_extreme_weather_data,
    },
    "arctic_ice": {
        "name": "Arctic & Polar Conditions",
        "icon": "🧊",
        "description": "Temperature & snowfall for 6 polar regions",
        "color": "#3498db",
        "func": get_arctic_ice_data,
    },
    "sea_level": {
        "name": "Sea Level",
        "icon": "🌊",
        "description": "Tidal data from 10 NOAA monitoring stations",
        "color": "#2980b9",
        "func": get_sea_level_data,
    },
    "us_climate": {
        "name": "US Climate",
        "icon": "🇺🇸",
        "description": "Weather data for 10 major US cities",
        "color": "#2c3e50",
        "func": get_us_climate_data,
    },
    "energy_transition": {
        "name": "Energy Transition",
        "icon": "⚡",
        "description": "US electricity generation by fuel type (2018-2023)",
        "color": "#f39c12",
        "func": lambda: get_energy_transition_data(os.getenv("EIA_API_KEY", "")),
    },
    "summary": {
        "name": "Full Summary Briefing",
        "icon": "📋",
        "description": "Run all agents and compile a complete climate briefing",
        "color": "#1abc9c",
        "func": get_summary,
    },
}


def capture_agent_output(agent_key):
    """Run an agent function and capture its printed output."""
    agent = AGENTS[agent_key]
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    try:
        agent["func"]()
    except Exception as exc:
        print(f"Error running agent: {exc}")
    finally:
        sys.stdout = old_stdout
    return buffer.getvalue()


@app.route("/")
def dashboard():
    agents_list = [
        {"key": k, **{f: v[f] for f in ("name", "icon", "description", "color")}}
        for k, v in AGENTS.items()
    ]
    return render_template("dashboard.html", agents=agents_list)


@app.route("/run/<agent_key>")
def run_agent_page(agent_key):
    if agent_key not in AGENTS:
        return "Agent not found", 404
    agent = AGENTS[agent_key]
    return render_template(
        "agent.html",
        agent_key=agent_key,
        agent_name=agent["name"],
        agent_icon=agent["icon"],
        agent_description=agent["description"],
        agent_color=agent["color"],
    )


@app.route("/api/run/<agent_key>")
def api_run_agent(agent_key):
    if agent_key not in AGENTS:
        return jsonify({"error": "Agent not found"}), 404
    output = capture_agent_output(agent_key)
    return jsonify({"agent": agent_key, "output": output})


if __name__ == "__main__":
    print("Climate Intelligence System — Web Interface")
    print("Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
