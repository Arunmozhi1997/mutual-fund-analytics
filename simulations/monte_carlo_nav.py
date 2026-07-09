import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load NAV data
file_path = "data/processed/nav_history_clean.csv"

df = pd.read_csv(file_path)


# Convert date column
df["date"] = pd.to_datetime(df["date"])


# Select one fund
fund_code = df["amfi_code"].iloc[0]

fund_data = df[
    df["amfi_code"] == fund_code
].sort_values("date")


print("Selected Fund:", fund_code)

print(fund_data.head())


# Calculate daily returns

fund_data["daily_return"] = (
    fund_data["nav"].pct_change()
)


returns = fund_data["daily_return"].dropna()


print("\nAverage Daily Return:")
print(returns.mean())

print("\nDaily Volatility:")
print(returns.std())

# ==============================
# Monte Carlo NAV Simulation
# ==============================

initial_nav = fund_data["nav"].iloc[-1]

days = 252 * 5       # 5 years of trading days
simulations = 1000


simulation_results = []


for i in range(simulations):

    nav_path = [initial_nav]

    current_nav = initial_nav

    for day in range(days):

        random_return = np.random.normal(
            returns.mean(),
            returns.std()
        )

        current_nav = current_nav * (1 + random_return)

        nav_path.append(current_nav)

    simulation_results.append(nav_path)


simulation_results = np.array(simulation_results)


print("\nInitial NAV:")
print(initial_nav)


print("\nExpected NAV after 5 years:")
print(np.percentile(simulation_results[:, -1], 50))


print("\nBest Case (95%):")
print(np.percentile(simulation_results[:, -1], 95))


print("\nWorst Case (5%):")
print(np.percentile(simulation_results[:, -1], 5))

# ==============================
# Plot Monte Carlo Results
# ==============================

plt.figure(figsize=(12,6))


# Confidence bands

median = np.percentile(
    simulation_results,
    50,
    axis=0
)

lower = np.percentile(
    simulation_results,
    5,
    axis=0
)

upper = np.percentile(
    simulation_results,
    95,
    axis=0
)


# Confidence area

plt.fill_between(
    range(days+1),
    lower,
    upper,
    alpha=0.3,
    label="90% Confidence Interval"
)


# Expected NAV

plt.plot(
    median,
    linewidth=2,
    label="Expected NAV"
)


plt.title(
    f"5-Year Monte Carlo NAV Forecast - Fund {fund_code}"
)

plt.xlabel(
    "Trading Days"
)

plt.ylabel(
    "NAV Value"
)


plt.legend()

plt.grid(True)

plt.show()