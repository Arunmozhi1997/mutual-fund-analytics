import pandas as pd 
import os
os.makedirs("data/processed", exist_ok=True)


#Fund Master
fund_master = pd.read_csv("data/raw/01_fund_master - Copy.csv")
print(fund_master.head())

fund_master = fund_master.drop_duplicates()

fund_master['launch_date'] = pd.to_datetime(
    fund_master['launch_date'],
    errors='coerce'
)
print(fund_master.dtypes)

fund_master.to_csv(
    "data/processed/fund_master_clean.csv",
    index=False
)

print("Fund Master Cleaned")

#NAV History
nav_history = pd.read_csv("data/raw/02_nav_history - Copy.csv")
print(nav_history.head())


