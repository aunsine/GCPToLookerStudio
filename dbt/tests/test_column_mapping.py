# tests/test_column_mapping.py

import pandas as pd
from main import sanitize_columns  # Assuming this function is in your main.py

def test_sanitize_columns_mapping():
    raw_columns = {
        "Property ID": [1],
        "Price GBP": [100000],
        "Listed Date": ["2025-07-08"],
        "Latitude": [51.5],
        "Longitude": [-0.1],
        "Property Type": ["Flat"]
    }

    df = pd.DataFrame(raw_columns)
    df = sanitize_columns(df)

    expected = [
        "property_id", "price_gbp", "listed_date",
        "latitude", "longitude", "property_type"
    ]
    assert list(df.columns) == expected, "Column mapping failed"