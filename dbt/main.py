# from google.cloud import bigquery

# # Create a BigQuery client instance
# client = bigquery.Client()

# # List datasets in your project
# datasets = list(client.list_datasets())
# project = client.project

# if datasets:
#     print(f"✅ Successfully authenticated! Datasets in project '{project}':")
#     for dataset in datasets:
#         print(f" - {dataset.dataset_id}")
# else:
#     print(f"⚠️ Authenticated to project '{project}', but no datasets found.")


import json
import os
import pandas as pd
from google.cloud import bigquery

# 1. Set your file paths (update as needed)
DATA_DIR = "dbt\input"
FILES = ["properties_1.txt", "properties_2.txt", "properties_3.txt"]

# 2. BigQuery setup
PROJECT_ID = "savvy-depot-465313-h2"
DATASET_ID = "rightmove_property"
TABLE_ID = "properties_raw"

client = bigquery.Client(project=PROJECT_ID)

# def load_json_split(file_path):
#     """Parse pandas-split JSON format into a DataFrame."""
#     with open(file_path, "r") as f:
#         raw = json.load(f)
#     df = pd.DataFrame(data=raw["data"], columns=raw["columns"])
#     return df
import json

def load_json_split(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()
        if not content:
            raise ValueError(f"Empty file: {file_path}")
        raw = json.loads(content)
    df = pd.DataFrame(data=raw["data"], columns=raw["columns"])
    return df


def ensure_table_exists(table_ref, schema):
    """Create BigQuery table if it doesn't exist."""
    try:
        client.get_table(table_ref)  # Check if table exists
        print(f"✅ Table '{TABLE_ID}' already exists.")
    except Exception:
        print(f"📦 Creating table '{TABLE_ID}'...")
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)
        print(f"✅ Table '{TABLE_ID}' created.")

def ingest_files():
    """Read all files and upload combined DataFrame to BigQuery."""
    all_dfs = []
    for file in FILES:
        file_path = os.path.join(DATA_DIR, file)
        print(f"Processing {file_path}...")
        df = load_json_split(file_path)
        all_dfs.append(df)

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Upload to BigQuery
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
        # Define schema (can be auto or explicit)
    schema = [
        bigquery.SchemaField("price", "FLOAT"),
        bigquery.SchemaField("type", "STRING"),
        bigquery.SchemaField("address", "STRING"),
        bigquery.SchemaField("url", "STRING"),

        bigquery.SchemaField("agent_url","STRING"),
        bigquery.SchemaField("number_bedrooms","INTEGER"),
        bigquery.SchemaField("agent_url","STRING"),
        bigquery.SchemaField("agent_url","STRING"),
        bigquery.SchemaField("agent_url","STRING"),
        bigquery.SchemaField("agent_url","STRING"),
        bigquery.SchemaField("agent_url","STRING"),
        
        bigquery.SchemaField("longitude", "FLOAT"),
        bigquery.SchemaField("property_type", "STRING"),
    ]

(['price', 'type', 'address', 'url', 'agent_url', 'number_bedrooms',
       'Full Description', 'Agent Name', 'Agent Address', 'postcode',
       'longitude', 'latitude', 'viewType', 'propertyType', 'propertySubType',
       'added', 'maxSizeFt', 'retirement', 'preOwned', 'file_name',
       'import_datetime'],
      dtype='object')
    ensure_table_exists(table_ref, schema)

    print(f"table ref: {table_ref}")
    job = client.load_table_from_dataframe(combined_df, table_ref)
    job.result()
    print(f"Uploaded {len(combined_df)} records to {table_ref}")

if __name__ == "__main__":
    ingest_files()