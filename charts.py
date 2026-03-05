"""Chart generation for Climate Intelligence System using matplotlib + pandas."""

import io
import base64
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for server use
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Consistent dark theme for all charts
DARK_BG = "#0f1923"
CARD_BG = "#172a3a"
TEXT_COLOR = "#e0e0e0"
GRID_COLOR = "#1e3a5f"
ACCENT_COLORS = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12",
    "#9b59b6", "#1abc9c", "#e67e22", "#2980b9",
]


def _fig_to_base64(fig):
    """Convert a matplotlib figure to a base64-encoded PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                facecolor=DARK_BG, edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def _apply_dark_style(ax):
    """Apply the dark theme to an axes object."""
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, alpha=0.5, linewidth=0.5)


def temperature_comparison_chart(data):
    """Bar chart comparing high/low temps across cities."""
    if not data:
        return None
    df = pd.DataFrame(data)
    # Take latest date per city
    df = df.sort_values("date").groupby("city").last().reset_index()
    df = df.sort_values("temp_max", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    y = np.arange(len(df))
    height = 0.35
    ax.barh(y + height/2, df["temp_max"], height, label="High", color="#e74c3c", alpha=0.85)
    ax.barh(y - height/2, df["temp_min"], height, label="Low", color="#3498db", alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(df["city"], fontsize=8)
    ax.set_xlabel("Temperature (°F)")
    ax.set_title("Global Temperature Comparison")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    return _fig_to_base64(fig)


def emissions_chart(data):
    """Grouped bar chart of air quality pollutants by city."""
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df.dropna(subset=["pm25"])

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    x = np.arange(len(df))
    w = 0.2
    ax.bar(x - 1.5*w, df["co"].fillna(0) / 100, w, label="CO (×100)", color="#e74c3c", alpha=0.85)
    ax.bar(x - 0.5*w, df["no2"].fillna(0), w, label="NO2", color="#3498db", alpha=0.85)
    ax.bar(x + 0.5*w, df["so2"].fillna(0), w, label="SO2", color="#2ecc71", alpha=0.85)
    ax.bar(x + 1.5*w, df["pm25"].fillna(0), w, label="PM2.5", color="#f39c12", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(df["city"], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("μg/m³")
    ax.set_title("Air Quality — Pollutant Levels by City")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR, fontsize=8)

    return _fig_to_base64(fig)


def us_climate_chart(data):
    """Temperature range chart for US cities."""
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df.sort_values("date").groupby("city").last().reset_index()
    df = df.sort_values("temp_max", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    y = np.arange(len(df))
    ranges = df["temp_max"] - df["temp_min"]
    ax.barh(y, ranges, left=df["temp_min"], color="#1abc9c", alpha=0.8)
    for i, row in df.iterrows():
        idx = list(df.index).index(i)
        ax.text(row["temp_min"] - 1, idx, f'{row["temp_min"]:.0f}°',
                va="center", ha="right", color=TEXT_COLOR, fontsize=7)
        ax.text(row["temp_max"] + 1, idx, f'{row["temp_max"]:.0f}°',
                va="center", ha="left", color=TEXT_COLOR, fontsize=7)

    ax.set_yticks(y)
    ax.set_yticklabels(df["city"], fontsize=8)
    ax.set_xlabel("Temperature (°F)")
    ax.set_title("US Cities — Temperature Range")

    return _fig_to_base64(fig)


def arctic_chart(data):
    """Line chart of arctic region temperatures over time."""
    if not data:
        return None
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    for i, (region, group) in enumerate(df.groupby("region")):
        group = group.sort_values("date")
        color = ACCENT_COLORS[i % len(ACCENT_COLORS)]
        ax.plot(group["date"], group["temp_max"], marker="o", label=region,
                color=color, linewidth=2, markersize=4)

    ax.set_ylabel("High Temperature (°F)")
    ax.set_title("Polar Region Temperatures")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR,
              fontsize=7, loc="best")
    plt.xticks(rotation=45, ha="right")

    return _fig_to_base64(fig)


def extreme_weather_chart(data):
    """Precipitation timeline for monitored cities."""
    if not data:
        return None
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    for i, (city, group) in enumerate(df.groupby("city")):
        group = group.sort_values("date")
        color = ACCENT_COLORS[i % len(ACCENT_COLORS)]
        ax.plot(group["date"], group["precip"], marker="s", label=city,
                color=color, linewidth=2, markersize=4)

    ax.set_ylabel("Precipitation (in)")
    ax.set_title("7-Day Precipitation Trends")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR,
              fontsize=7, loc="best")
    plt.xticks(rotation=45, ha="right")

    return _fig_to_base64(fig)


def energy_chart(data):
    """Stacked bar chart of energy generation by fuel type over years."""
    if not data:
        return None
    df = pd.DataFrame(data)
    pivot = df.pivot_table(index="year", columns="fuel", values="generation",
                           aggfunc="sum").fillna(0)
    pivot = pivot.sort_index()

    fuel_colors = {
        "Solar": "#f39c12", "Wind": "#3498db", "Hydro": "#2ecc71",
        "Nuclear": "#9b59b6", "Coal": "#7f8c8d", "Natural Gas": "#e74c3c",
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    bottom = np.zeros(len(pivot))
    for fuel in pivot.columns:
        color = fuel_colors.get(fuel, "#95a5a6")
        ax.bar(pivot.index, pivot[fuel], bottom=bottom, label=fuel,
               color=color, alpha=0.85)
        bottom += pivot[fuel].values

    ax.set_ylabel("Generation (thousand MWh)")
    ax.set_title("US Electricity Generation by Fuel Type")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR,
              fontsize=8, loc="upper left")

    return _fig_to_base64(fig)


def sea_level_chart(data):
    """Bar chart of sea level heights by station."""
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df.dropna(subset=["height_m"])
    if df.empty:
        return None
    df = df.sort_values("height_m")

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(DARK_BG)
    _apply_dark_style(ax)

    colors = ["#e74c3c" if h > 0 else "#3498db" for h in df["height_m"]]
    ax.barh(df["station"], df["height_m"], color=colors, alpha=0.85)
    ax.set_xlabel("Height Above MSL (meters)")
    ax.set_title("Sea Level — Monthly Mean by Station")
    ax.axvline(x=0, color=TEXT_COLOR, linewidth=0.5, alpha=0.5)

    return _fig_to_base64(fig)


# Map chart names to their generator functions and the agent data source
CHART_REGISTRY = {
    "temperature": {
        "title": "Global Temperature Comparison",
        "func": temperature_comparison_chart,
        "agent": "temperature",
    },
    "emissions": {
        "title": "Air Quality Pollutant Levels",
        "func": emissions_chart,
        "agent": "emissions",
    },
    "us_climate": {
        "title": "US City Temperature Ranges",
        "func": us_climate_chart,
        "agent": "us_climate",
    },
    "arctic": {
        "title": "Polar Region Temperatures",
        "func": arctic_chart,
        "agent": "arctic_ice",
    },
    "extreme_weather": {
        "title": "7-Day Precipitation Trends",
        "func": extreme_weather_chart,
        "agent": "extreme_weather",
    },
    "energy": {
        "title": "US Energy Generation by Fuel",
        "func": energy_chart,
        "agent": "energy_transition",
    },
    "sea_level": {
        "title": "Sea Level by Station",
        "func": sea_level_chart,
        "agent": "sea_level",
    },
}
