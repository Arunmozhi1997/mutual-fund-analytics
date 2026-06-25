import pandas as pd

files = [
    "data/raw/01_fund_master - Copy.csv",
    "data/raw/02_nav_history - Copy.csv",
    "data/raw/07_scheme_performance - Copy.csv",
    "data/raw/08_investor_transactions - Copy.csv"
]

for file in files:
    print("\n" + "="*60)
    print(file)

    df = pd.read_csv(file)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nShape:")
    print(df.shape)

    print("\nFirst 3 rows:")
    print(df.head(3))