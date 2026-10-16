# Telemetry Data Cleaning, Aggregation & Visualization Suite

A modular, fault-tolerant Python solution for cleaning raw sensor streams, aggregating device telemetry logs, filtering thermal anomalies, and visualizing device metrics.

## Repository Structure

```text
device-telemetry-assessment/
├── README.md                  # Documentation and execution guide
├── PROMPT_LOG.md              # AI collaboration log for Question 3
├── requirements.txt           # External dependency (matplotlib)
├── data/
│   └── device_telemetry.csv   # Sample input telemetry dataset (includes edge cases)
├── output/
│   ├── sample_output.json     # Exported JSON from Question 2
│   └── sample_chart.png       # Generated bar chart from Question 3
└── src/
    ├── sensor_cleaning.py     # Question 1: Sensor normalization & unit tests
    ├── telemetry_processor.py # Question 2: CSV ingestion, aggregation & JSON export
    └── visualize_telemetry.py # Question 3: Matplotlib bar chart generator
```

## Quickstart & Verification

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Question 1: Clean and Normalize Sensor Readings
```bash
python src/sensor_cleaning.py
```
* **Highlights:** Converts mixed types to `float`, safely filters out `None`, negative flags, unparseable strings, Python `bool` values (`True`/`False`), and `NaN`/`Inf` literals, and caps values at `500.0`.

### 3. Run Question 2: Telemetry CSV Aggregation & Export
```bash
python src/telemetry_processor.py
```
* **Highlights:** Streams `data/device_telemetry.csv`, skips corrupted records without crashing, groups by `device_id`, filters out devices with an average temperature above `80.0°C`, prints a formatted terminal table, and writes `output/sample_output.json`.

### 4. Run Question 3: Bar Chart Visualization
```bash
python src/visualize_telemetry.py
```
* **Highlights:** Reads `output/sample_output.json` and saves a 300 DPI bar chart to `output/sample_chart.png` with dynamic y-axis headroom and data annotations.
