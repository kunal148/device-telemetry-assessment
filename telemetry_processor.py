"""
Module: telemetry_processor.py
Description: Ingests device_telemetry.csv, computes per-device metrics, filters out
             devices with average temperature > 80.0, exports JSON, and prints a summary table.
"""

import csv
import json
import math
import os
import sys
from typing import Any, Dict, List


def process_device_telemetry(
    csv_path: str = "data/device_telemetry.csv",
    output_json_path: str = "output/sample_output.json",
    max_avg_temp: float = 80.0,
) -> List[Dict[str, Any]]:
    """
    Reads telemetry CSV data, aggregates statistics by device_id, filters out devices
    with an average temperature above max_avg_temp, and saves the result to JSON.
    """
    if not os.path.exists(csv_path):
        print(f"[ERROR] Input CSV file not found at '{csv_path}'.", file=sys.stderr)
        return []

    device_groups: Dict[str, Dict[str, Any]] = {}
    skipped_rows = 0

    try:
        with open(csv_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            required_columns = {"device_id", "status", "temperature"}
            if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
                print(
                    f"[ERROR] CSV is missing required columns: {required_columns}",
                    file=sys.stderr,
                )
                return []

            for row in reader:
                raw_device_id = row.get("device_id")
                raw_status = row.get("status")
                raw_temp = row.get("temperature")

                if not raw_device_id or not raw_device_id.strip():
                    skipped_rows += 1
                    continue

                device_id = raw_device_id.strip()

                try:
                    temperature = float(raw_temp)  # type: ignore[arg-type]
                    if math.isnan(temperature) or math.isinf(temperature):
                        skipped_rows += 1
                        continue
                except (ValueError, TypeError):
                    skipped_rows += 1
                    continue

                status = (raw_status or "").strip().upper()

                if device_id not in device_groups:
                    device_groups[device_id] = {
                        "total_records": 0,
                        "temp_sum": 0.0,
                        "error_count": 0,
                    }

                device_groups[device_id]["total_records"] += 1
                device_groups[device_id]["temp_sum"] += temperature
                if status == "ERROR":
                    device_groups[device_id]["error_count"] += 1

    except OSError as err:
        print(f"[ERROR] Failed to read CSV file '{csv_path}': {err}", file=sys.stderr)
        return []

    # Aggregate and filter out devices with average temperature > 80.0
    aggregated_results: List[Dict[str, Any]] = []

    for device_id, stats in sorted(device_groups.items()):
        total_records = stats["total_records"]
        if total_records == 0:
            continue

        avg_temp = round(stats["temp_sum"] / total_records, 2)

        if avg_temp <= max_avg_temp:
            aggregated_results.append(
                {
                    "device_id": device_id,
                    "total_records": total_records,
                    "average_temperature": avg_temp,
                    "error_count": stats["error_count"],
                }
            )

    # Export to JSON
    try:
        output_dir = os.path.dirname(output_json_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_json_path, mode="w", encoding="utf-8") as json_file:
            json.dump(aggregated_results, json_file, indent=4)
    except OSError as err:
        print(f"[ERROR] Failed to write JSON file '{output_json_path}': {err}", file=sys.stderr)

    # Print summary table in the terminal
    print("\n" + "=" * 68)
    print(f"DEVICE TELEMETRY SUMMARY (Filtered: Avg Temperature <= {max_avg_temp:.1f}°C)")
    print("=" * 68)
    print(f"{'Device ID':<14} | {'Total Records':<15} | {'Avg Temp (°C)':<15} | {'Error Count':<12}")
    print("-" * 68)

    if not aggregated_results:
        print("No devices matched the filtering criteria.")
    else:
        for item in aggregated_results:
            print(
                f"{item['device_id']:<14} | "
                f"{item['total_records']:<15} | "
                f"{item['average_temperature']:<15.2f} | "
                f"{item['error_count']:<12}"
            )

    print("=" * 68)
    if skipped_rows > 0:
        print(f"Note: Safely skipped {skipped_rows} malformed row(s) during CSV ingestion.")
    print(f"Saved clean JSON output to: {output_json_path}\n")

    return aggregated_results


if __name__ == "__main__":
    process_device_telemetry()
