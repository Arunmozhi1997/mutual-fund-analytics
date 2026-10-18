import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "processed")
sharpe = pd.read_csv(os.path.join(DATA_DIR, "sharpe_ratio.csv"))
fund = pd.read_csv(os.path.join(DATA_DIR, "fund_master_clean.csv"))
recommendation_data = sharpe.merge(
    fund[["amfi_code", "risk_category"]],
    on="amfi_code",
    how="left"
)

# Take user input
risk = input("Enter risk appetite (Low / Moderate / High): ").strip()

# Filter and recommend
recommendations = (
    recommendation_data[
        recommendation_data["risk_category"].str.lower() == risk.lower()
    ]
    .sort_values(by="sharpe_ratio", ascending=False)
    .head(3)
)

# result
if recommendations.empty:
    print("\nNo funds found for this risk appetite.")
else:
    print("\nTop 3 Recommended Funds\n")
    print(
        recommendations[
            ["scheme_name", "risk_category", "sharpe_ratio"]
        ].to_string(index=False)
    )
