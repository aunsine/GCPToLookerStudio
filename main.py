import os
import json
import pandas as pd
from google.cloud import bigquery

# CONFIGURATION 🛠️
DATA_DIR = "input"
FILES = ["properties_1.txt", "properties_2.txt", "properties_3.txt"]

PROJECT_ID = "savvy-depot-465313-h2"
DATASET_ID = "rightmove_property"
TABLE_ID = "raw_properties"
TABLE_REF = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

client = bigquery.Client(project=PROJECT_ID)

# Start Utility Functions
def load_json_split(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        raw = json.loads(f.read().strip())
    return pd.DataFrame(data=raw["data"], columns=raw["columns"])

def sanitize_columns(df):
    """Sanitize DataFrame column names to be BigQuery compatible."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )
    return df

def ensure_table_exists(schema):
    """Ensure the BigQuery table exists, creating it if necessary."""
    try:
        client.get_table(TABLE_REF)
        print(f"Table '{TABLE_ID}' exists.")
    except Exception:
        print(f"📦 Creating table '{TABLE_ID}'...")
        table = bigquery.Table(TABLE_REF, schema=schema)
        client.create_table(table)
        print(f"Table '{TABLE_ID}' created.")

def align_types(df, schema_fields, auto_cast=True):
    """Align DataFrame types with BigQuery schema."""
    df = df.copy()
    type_map = {
        "STRING": str,
        "INTEGER": "Int64",
        "FLOAT": "float64",
        "BOOLEAN": "bool",
        "TIMESTAMP": "datetime64[ns]",
        "DATE": "datetime64[ns]",
    }

    schema_dict = {field.name: field.field_type for field in schema_fields}
    for col in df.columns:
        expected_type = schema_dict.get(col)
        if expected_type:
            target_type = type_map.get(expected_type)
            if target_type:
                try:
                    if expected_type in ["TIMESTAMP", "DATE"]:
                        df[col] = pd.to_datetime(df[col], errors="coerce")
                    else:
                        df[col] = df[col].astype(target_type)
                except Exception as e:
                    print(f"Error casting '{col}' → {expected_type}: {e}")
    return df

def infer_schema(df):
    """Infer BigQuery schema from DataFrame."""
    gbq_schema = []
    for col, dtype in df.dtypes.items():
        if "int" in str(dtype):
            gbq_type = "INTEGER"
        elif "float" in str(dtype):
            gbq_type = "FLOAT"
        elif "bool" in str(dtype):
            gbq_type = "BOOLEAN"
        elif "datetime" in str(dtype):
            gbq_type = "TIMESTAMP"
        else:
            gbq_type = "STRING"
        gbq_schema.append(bigquery.SchemaField(col, gbq_type))
    return gbq_schema

def ingest_files(file_list):
    all_dataframes = []
    for file in file_list:
        path = os.path.join(DATA_DIR, file)
        print(f"Loading {file}...")
        df = load_json_split(path)
        df = sanitize_columns(df)
        df["input_file_name"] = file                        # Added file name
        df["import_timestamp"] = pd.Timestamp.now(tz="UTC") # Added import timestamp for each file.
        all_dataframes.append(df)
    return pd.concat(all_dataframes, ignore_index=True)
# End Utility Functions

def main():
    print("Starting ingestion...")
    combined_df = ingest_files(FILES)       #Ingest file and added 2 additional columns: `input_file_name` and `import_timestamp`.
    gbq_schema = infer_schema(combined_df)  # Infer schema from the combined DataFrame
    
    ensure_table_exists(gbq_schema)         # Ensure the table exists with the inferred schema, if not create it.
    
    combined_df = align_types(combined_df, gbq_schema) # Align DataFrame types with BigQuery schema

    job = client.load_table_from_dataframe(combined_df, TABLE_REF)
    job.result()

    print(f"Uploaded {len(combined_df)} records from {len(FILES)} files to {TABLE_REF}")

if __name__ == "__main__":
    main()