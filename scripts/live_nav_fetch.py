from pathlib import Path
from datetime import datetime
import logging
import requests
import pandas as pd

# Create output folder
OUTPUT_FOLDER = Path("data/raw")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Create logs folder
LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FOLDER / "etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Mutual Fund Scheme Codes
schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

print("=" * 50)
print("Starting Daily NAV Update")
print("=" * 50)

logging.info("Daily NAV Update Started")

for scheme_name, scheme_code in schemes.items():

    try:
        print(f"Fetching {scheme_name}...")

        url = f"https://api.mfapi.in/mf/{scheme_code}"

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        file_path = OUTPUT_FOLDER / f"{scheme_name}_live_nav.csv"

        nav_df.to_csv(file_path, index=False)

        print(f"✓ Saved {file_path}")

        logging.info(f"{scheme_name} downloaded successfully.")

    except Exception as e:
        print(f"✗ Failed to download {scheme_name}")
        print(e)
        logging.error(f"{scheme_name} failed: {e}")

print("\nDaily NAV Update Completed Successfully!")
logging.info("Daily NAV Update Completed")