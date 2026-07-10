import pandas as pd
from datetime import datetime
from pathlib import Path


# Load NAV data
df = pd.read_csv("data/processed/nav_history_clean.csv")

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")



# Create pivot table
pivot = df.pivot(
    index="date",
    columns="amfi_code",
    values="nav"
)

pivot = pivot.ffill()



# Calculate daily returns
returns = pivot.pct_change(fill_method=None).dropna()

# Calculate annual returns
annual_returns = returns.mean() * 252

total_funds = pivot.shape[1]

avg_return = annual_returns.mean()

top5 = annual_returns.sort_values(ascending=False).head(5)


# Best performing fund
best_fund = annual_returns.idxmax()
best_return = annual_returns.max()

print("\nBest Performing Fund")
print(f"Fund: {best_fund}")
print(f"Annual Return: {best_return:.2%}")

rows = ""

for fund, ret in top5.items():
    rows += f"""
    <tr>
        <td>{fund}</td>
        <td>{ret:.2%}</td>
    </tr>
    """

# Create HTML report
html_content = f"""
<html>

<head>

<title>Weekly Mutual Fund Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: white;
    color: black;
}}

h1 {{
    color: #0066cc;
}}

h2 {{
    color: #333333;
}}

p {{
    color: black;
}}

table {{
    width: 60%;
    border-collapse: collapse;
    background-color: white;
}}

th {{
    background-color: #0066cc;
    color: white;
    border: 1px solid #cccccc;
    padding: 10px;
    text-align: left;
}}

td {{
    background-color: white;
    color: black;
    border: 1px solid #cccccc;
    padding: 10px;
}}

hr {{
    border: 1px solid #dddddd;
}}

</style>

</head>

<body>

<h1>📈 Weekly Mutual Fund Performance Report</h1>

<hr>

<p><strong>Total Funds:</strong> {total_funds}</p>

<p><strong>Average Annual Return:</strong> {avg_return:.2%}</p>

<hr>

<h2>🏆 Best Performing Fund</h2>

<p><strong>Fund Code:</strong> {best_fund}</p>

<p><strong>Annual Return:</strong> {best_return:.2%}</p>

<hr>

<h2>Top 5 Funds</h2>

<table>

<tr>
<th>Fund Code</th>
<th>Annual Return</th>
</tr>

{rows}

</table>

<hr>

<p>Generated on: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>

</body>

</html>
"""


# Save HTML report
report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

output_file = report_dir / "weekly_report.html"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print("\nHTML report generated successfully!")