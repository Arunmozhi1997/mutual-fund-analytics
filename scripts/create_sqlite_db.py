from pathlib import Path
import sqlite3
import pandas as pd

# ----------------------------------
# Project Paths
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_DIR = BASE_DIR / "data" / "db"

DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "bluestock_mf.db"

# ----------------------------------
# Connect to SQLite
# ----------------------------------
conn = sqlite3.connect(DB_PATH)

print(f"\nCreating database...\n{DB_PATH}\n")

# ----------------------------------
# Import every processed CSV
# ----------------------------------
csv_files = sorted(PROCESSED_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in {PROCESSED_DIR}"
    )

for csv in csv_files:

    table_name = csv.stem

    print(f"Loading {csv.name}")

    df = pd.read_csv(csv)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

print("\nAll tables imported successfully.")

# ----------------------------------
# Display tables
# ----------------------------------
tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """,
    conn
)

print("\nTables in SQLite Database:\n")
print(tables)

conn.close()

print("\nDatabase created successfully!")
print(DB_PATH)