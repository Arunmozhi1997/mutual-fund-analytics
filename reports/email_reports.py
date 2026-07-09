import pandas as pd
from datetime import datetime


# Load NAV data
df = pd.read_csv("data/processed/nav_history_clean.csv")

df["date"] = pd.to_datetime(df["date"])

print(df.head())

# Create pivot table
pivot = df.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

print("\nPivot Table:")
print(pivot.head())

# Calculate daily returns
returns = pivot.pct_change().dropna()

print("\nDaily Returns:")
print(returns.head())

# Calculate annual returns
annual_returns = returns.mean() * 252

print("\nAnnual Returns:")
print(annual_returns.head())

# Best performing fund
best_fund = annual_returns.idxmax()
best_return = annual_returns.max()

print("\nBest Performing Fund")
print(f"Fund: {best_fund}")
print(f"Annual Return: {best_return:.2%}")

# Create HTML report
html_content = f"""
<html>
<head>
    <title>Weekly Mutual Fund Report</title>
</head>
<body>
    <h1>📈 Weekly Mutual Fund Performance Report</h1>

    <hr>

    <h2>Best Performing Fund</h2>

    <p><strong>Fund Code:</strong> {best_fund}</p>

    <p><strong>Annual Return:</strong> {best_return:.2%}</p>

    <hr>

    <p>Generated on: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>

</body>
</html>
"""

# Save HTML report
with open("reports/weekly_report.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("\nHTML report generated successfully!")