# AI Collaboration & Prompt Log (`PROMPT_LOG.md`)

## Scope of AI Usage
- **Question 1 (`src/sensor_cleaning.py`):** Written manually without AI assistance, per assessment instructions.
- **Question 2 (`src/telemetry_processor.py`):** Written manually without AI assistance using Python's standard `csv` and `json` libraries.
- **Question 3 (`src/visualize_telemetry.py`):** Generated initial plotting code using an AI assistant, reviewed the output for layout/robustness flaws, and iterated to produce the final script.

---

## 1. Initial Prompt to the AI Assistant

> "Write a Python script using `matplotlib` that loads a JSON file from `output/sample_output.json` containing a list of objects with keys `device_id`, `total_records`, `average_temperature`, and `error_count`. Plot a bar chart comparing `average_temperature` per `device_id`, show the temperature value on top of each bar, and save the chart to `output/sample_chart.png`."

---

## 2. Bugs & Formatting Mistakes Found in the AI's First Attempt

When I reviewed and ran the AI's initial code, I identified two issues:
1. **Overlapping Bar Labels with the Top Border (Layout Bug):** The AI placed text annotations above each bar using `plt.text()` without increasing the y-axis upper limit (`plt.ylim`). Because `DEV_D` had an average temperature of `79.67°C`, the text label above `DEV_D` collided directly with the top frame border of the plot. It also omitted `plt.tight_layout()`, causing clipped axis margins.
2. **Missing File & Empty Data Guards (Robustness Bug):** The initial script called `open('output/sample_output.json')` directly without checking if the file existed or handling corrupted/empty JSON arrays, which would cause an unhandled crash if the upstream pipeline failed.

---

## 3. Follow-Up Prompt Used to Fix It

> "The temperature label on top of the tallest bar (`79.7°C`) overlaps with the top border of the chart, and the script crashes if the JSON file is missing or empty. Please update the script to:
> 1. Dynamically set `plt.ylim(0, max(avg_temps) * 1.15)` to add 15% vertical headroom above the tallest bar so annotations never touch the top border.
> 2. Add a clear chart title, axis labels with `°C` units, horizontal dashed gridlines, and `plt.tight_layout()` before saving at 300 DPI.
> 3. Add error handling for missing files (`os.path.exists`), `json.JSONDecodeError`, and empty JSON lists."
