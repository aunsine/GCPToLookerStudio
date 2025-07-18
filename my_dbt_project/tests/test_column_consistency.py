import os
import sys
import json
import pandas as pd
import pytest
from main import sanitize_columns, load_json_split

DATA_DIR = "input/"
FILES = ["properties_1.txt", "properties_2.txt", "properties_3.txt"]

EXPECTED_COLUMNS = [   
"price",
"type",
"address",
"url",
"agent_url",
"number_bedrooms",
"full_description",
"agent_name",
"agent_address",
"postcode",
"longitude",
"latitude",
"viewtype",
"propertytype",
"propertysubtype",
"added",
"maxsizeft",
"retirement",
"preowned",
]

@pytest.mark.parametrize("filename", FILES)
def test_columns_match_expected(filename):

    print(f"Actual testing file: {os.path.join(DATA_DIR, filename)}")
    actual = load_json_split(os.path.join(DATA_DIR, filename))    
    cleaned = [c.strip().lower().replace(" ", "_") for c in actual]
    assert cleaned == EXPECTED_COLUMNS, f"Mismatch in columns: {filename}"