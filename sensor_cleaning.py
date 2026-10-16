"""
Module: sensor_cleaning.py
Description: Clean and normalize mixed-type sensor readings (Question 1).
"""

import math
from typing import Any, Iterable, List, Optional


def clean_sensor_readings(readings: Optional[Iterable[Any]]) -> List[float]:
    """
    Cleans and normalizes a list of mixed sensor inputs into valid floats.

    Steps applied:
    1. Type Conversion & Filtering: Converts valid elements to floats. Drops None,
       booleans (preventing bool-to-float coercion), unparseable strings,
       non-finite numbers (NaN, Inf), and negative error flags (< 0.0).
    2. Clipping: Caps any valid reading exceeding 500.0 at 500.0.
    3. Edge Case Handling: Handles None, empty lists, or lists with all-invalid
       entries gracefully without throwing unhandled exceptions.
    """
    if not readings or not isinstance(readings, (list, tuple)):
        return []

    cleaned_readings: List[float] = []

    for item in readings:
        # Explicitly reject None and booleans (since bool is a subclass of int in Python)
        if item is None or isinstance(item, bool):
            continue

        try:
            value = float(item)
        except (ValueError, TypeError):
            continue

        # Drop NaN, Infinity, or negative error flags (< 0)
        if math.isnan(value) or math.isinf(value) or value < 0.0:
            continue

        # Clip values exceeding 500.0
        if value > 500.0:
            value = 500.0

        cleaned_readings.append(value)

    return cleaned_readings


if __name__ == "__main__":
    # Test Case 1: Mixed valid numbers, numeric strings, None, negatives, error strings, and >500 spikes
    test_1_input = [23.5, "45.0", None, -10.0, "ERR_404", 612.8, 0.0, True]
    test_1_result = clean_sensor_readings(test_1_input)
    print(f"Test Case 1 (Mixed Inputs):      {test_1_result}")
    assert test_1_result == [23.5, 45.0, 500.0, 0.0], "Test Case 1 Failed"

    # Test Case 2: Empty list edge case
    test_2_input: List[Any] = []
    test_2_result = clean_sensor_readings(test_2_input)
    print(f"Test Case 2 (Empty List):        {test_2_result}")
    assert test_2_result == [], "Test Case 2 Failed"

    # Test Case 3: Entirely invalid entries (corrupt strings, nulls, negative flags, NaN)
    test_3_input = [None, "offline", -1.0, -999, "NaN", False]
    test_3_result = clean_sensor_readings(test_3_input)
    print(f"Test Case 3 (All Invalid):       {test_3_result}")
    assert test_3_result == [], "Test Case 3 Failed"

    print("\nAll test cases passed successfully.")
