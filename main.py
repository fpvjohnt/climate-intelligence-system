import os
import sys
import argparse
from dotenv import load_dotenv

# Load API keys
load_dotenv("config/.env")

NOAA_KEY = os.getenv("NOAA_API_KEY")
EIA_KEY = os.getenv("EIA_API_KEY")
NASA_TOKEN = os.getenv("NASA_EARTHDATA_TOKEN")
FIRMS_KEY = os.getenv("NASA_FIRMS_MAP_KEY")

def print_status():
    print("Climate Intelligence System v2.0")
    print("=" * 40)
    print(f"NOAA key loaded:  {'✅' if NOAA_KEY else '❌'}")
    print(f"EIA key loaded:   {'✅' if EIA_KEY else '❌'}")
    print(f"NASA key loaded:  {'✅' if NASA_TOKEN else '❌'}")
    print(f"FIRMS key loaded: {'✅' if FIRMS_KEY else '❌ (optional — wildfire satellite data)'}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Climate Intelligence System")
    parser.add_argument("--mode", choices=["full", "alerts", "risk", "export"],
                        default="full", help="Run mode")
    args = parser.parse_args()

    print_status()

    if args.mode == "full":
        from agents.summary_agent import get_summary
        get_summary()

    elif args.mode == "alerts":
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
        from alert_system import check_alerts
        alerts = check_alerts()
        from data_exporter import export_alerts
        print("\n📦 Exporting alerts...")
        export_alerts(alerts)

    elif args.mode == "risk":
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
        from climate_risk_scorer import compute_risk_scores
        results = compute_risk_scores()
        from data_exporter import export_risk_scores
        print("\n📦 Exporting risk scores...")
        export_risk_scores(results)

    elif args.mode == "export":
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
        from climate_risk_scorer import compute_risk_scores
        from alert_system import check_alerts
        from data_exporter import export_risk_scores, export_alerts
        print("Running risk scoring...")
        risk_results = compute_risk_scores()
        print("\nRunning alert checks...")
        alerts = check_alerts()
        print("\n📦 Exporting all data...")
        export_risk_scores(risk_results)
        export_alerts(alerts)

if __name__ == "__main__":
    main()
