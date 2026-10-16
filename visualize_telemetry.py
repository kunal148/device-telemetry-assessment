"""
Module: visualize_telemetry.py
Description: Loads the aggregated JSON output from Question 2 and generates a bar chart
             comparing average temperature per device using matplotlib.
"""

import json
import os
import sys
from typing import Any, Dict, List

import matplotlib.pyplot as plt


def plot_device_temperatures(
    json_path: str = "output/sample_output.json",
    output_chart_path: str = "output/sample_chart.png",
) -> bool:
    """
    Loads filtered device telemetry metrics from JSON and renders a formatted bar chart.
    """
    if not os.path.exists(json_path):
        print(f"[ERROR] JSON input file not found at '{json_path}'.", file=sys.stderr)
        return False

    try:
        with open(json_path, mode="r", encoding="utf-8") as file:
            data: List[Dict[str, Any]] = json.load(file)
    except (json.JSONDecodeError, OSError) as err:
        print(f"[ERROR] Could not read or parse JSON file '{json_path}': {err}", file=sys.stderr)
        return False

    if not data:
        print("[WARNING] JSON dataset is empty. No chart generated.", file=sys.stderr)
        return False

    device_ids = [str(record.get("device_id", "N/A")) for record in data]
    avg_temps = [float(record.get("average_temperature", 0.0)) for record in data]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(
        device_ids,
        avg_temps,
        color="#2b5c8f",
        edgecolor="#16324f",
        width=0.5,
    )

    # Add exact temperature labels above each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"{height:.1f}°C",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    plt.title(
        "Average Device Temperature Comparison (Filtered <= 80.0°C)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    plt.xlabel("Device ID", fontsize=11, labelpad=8)
    plt.ylabel("Average Temperature (°C)", fontsize=11, labelpad=8)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Add 15% vertical headroom so bar value labels do not overlap the top chart border
    max_temp = max(avg_temps) if avg_temps else 80.0
    plt.ylim(0, max(max_temp * 1.15, 10.0))

    plt.tight_layout()

    try:
        output_dir = os.path.dirname(output_chart_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(output_chart_path, dpi=300)
        plt.close()
        print(f"Chart successfully saved to: {output_chart_path}")
        return True
    except OSError as err:
        print(f"[ERROR] Failed to save chart to '{output_chart_path}': {err}", file=sys.stderr)
        return False


if __name__ == "__main__":
    plot_device_temperatures()
