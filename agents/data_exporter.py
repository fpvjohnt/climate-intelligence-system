import json
import csv
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_risk_scores(risk_results):
    """Export climate risk scores to JSON and CSV."""
    if not risk_results:
        print("⚠️ No risk data to export")
        return

    ensure_output_dir()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # JSON export
    json_path = os.path.join(OUTPUT_DIR, f"risk_scores_{timestamp}.json")
    export_data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_locations": len(risk_results),
        "results": risk_results,
    }
    with open(json_path, "w") as f:
        json.dump(export_data, f, indent=2)
    print(f"📁 JSON: {json_path}")

    # CSV export
    csv_path = os.path.join(OUTPUT_DIR, f"risk_scores_{timestamp}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "location", "lat", "lon", "composite_score", "risk_level",
            "heat_score", "precipitation_score", "wind_score", "air_quality_score",
            "drought_score", "uv_score", "humidity_score",
            "temp_max_c", "precip_today_mm", "precip_14d_mm", "wind_max_kmh",
            "uv_index", "humidity_pct", "soil_moisture", "pm25"
        ])
        for r in risk_results:
            scores = r.get("scores", {})
            raw = r.get("raw", {})
            writer.writerow([
                r["location"], r["lat"], r["lon"],
                r["composite_score"], r["risk_level"],
                scores.get("heat", ""), scores.get("precipitation", ""),
                scores.get("wind", ""), scores.get("air_quality", ""),
                scores.get("drought", ""), scores.get("uv", ""),
                scores.get("humidity", ""),
                raw.get("temp_max_c", ""), raw.get("precip_today_mm", ""),
                raw.get("precip_14d_mm", ""), raw.get("wind_max_kmh", ""),
                raw.get("uv_index", ""), raw.get("humidity_pct", ""),
                raw.get("soil_moisture", ""), raw.get("pm25", ""),
            ])
    print(f"📁 CSV:  {csv_path}")
    return json_path, csv_path

def export_alerts(alerts):
    """Export alert data to JSON and CSV."""
    if not alerts:
        print("⚠️ No alert data to export")
        return

    ensure_output_dir()
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # JSON
    json_path = os.path.join(OUTPUT_DIR, f"alerts_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_alerts": len(alerts),
            "alerts": alerts,
        }, f, indent=2)
    print(f"📁 JSON: {json_path}")

    # CSV
    csv_path = os.path.join(OUTPUT_DIR, f"alerts_{timestamp}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["location", "date", "alert", "severity", "value", "threshold", "unit"])
        for a in alerts:
            writer.writerow([
                a["location"], a["date"], a["alert"],
                a["severity"], a["value"], a["threshold"], a["unit"],
            ])
    print(f"📁 CSV:  {csv_path}")
    return json_path, csv_path

if __name__ == "__main__":
    print("Data Exporter — use export_risk_scores() or export_alerts() with data from other agents.")
