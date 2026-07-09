import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("data/processed/nav_history_clean.csv")

df["date"] = pd.to_datetime(df["date"])

print(df["amfi_code"].unique()[:10])

selected_funds = [
    100016,
    100025,
    100033,
    101206,
    101207
]

fund_data = df[df["amfi_code"].isin(selected_funds)]

print(fund_data.head())

# Create pivot table
pivot = fund_data.pivot(
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
mean_returns = returns.mean() * 252

print("\nAnnual Returns:")
print(mean_returns)

# Calculate annual covariance matrix
cov_matrix = returns.cov() * 252

print("\nAnnual Covariance Matrix:")
print(cov_matrix)

# ==============================
# Markowitz Portfolio Simulation
# ==============================

num_portfolios = 5000

results = []

weights_list = []

for i in range(num_portfolios):

    # Generate random weights
    weights = np.random.random(len(selected_funds))

    # Make sure weights sum to 1
    weights /= np.sum(weights)

        # Calculate portfolio return
    portfolio_return = np.sum(weights * mean_returns)

    # Calculate portfolio risk (volatility)
    portfolio_risk = np.sqrt(
        np.dot(
            weights.T,
            np.dot(cov_matrix, weights)
        )
    )

    # Calculate Sharpe Ratio (risk-free rate = 0)
    sharpe_ratio = portfolio_return / portfolio_risk

    # Store the results
    results.append([
        portfolio_return,
        portfolio_risk,
        sharpe_ratio
    ])

    # Store the portfolio weights
    weights_list.append(weights)

print("\nNumber of portfolios created:")
print(len(results))

print("\nFirst portfolio:")
print(results[0])

# Convert results to DataFrame
results_df = pd.DataFrame(
    results,
    columns=[
        "Return",
        "Risk",
        "Sharpe"
    ]
)

print("\nPortfolio Results:")
print(results_df.head())

# Portfolio with highest Sharpe Ratio
max_sharpe = results_df["Sharpe"].idxmax()

best_portfolio = results_df.loc[max_sharpe]

print("\nBest Portfolio (Maximum Sharpe Ratio):")
print(best_portfolio)

# Portfolio with lowest risk
min_risk = results_df["Risk"].idxmin()

lowest_risk_portfolio = results_df.loc[min_risk]

print("\nMinimum Risk Portfolio:")
print(lowest_risk_portfolio)

# Print Best Portfolio Weights
print("\nBest Portfolio Weights")

best_weights = weights_list[max_sharpe]

for fund, weight in zip(selected_funds, best_weights):
    print(f"Fund {fund}: {weight:.2%}")

# Print Minimum Risk Portfolio Weights
print("\nMinimum Risk Portfolio Weights")

min_weights = weights_list[min_risk]

for fund, weight in zip(selected_funds, min_weights):
    print(f"Fund {fund}: {weight:.2%}")

# Plot Efficient Frontier
plt.figure(figsize=(12, 8))

# Scatter plot of all portfolios
plt.scatter(
    results_df["Risk"],
    results_df["Return"],
    c=results_df["Sharpe"],
    cmap="viridis",
    alpha=0.6
)

# Color bar
plt.colorbar(label="Sharpe Ratio")

# Highlight Maximum Sharpe Portfolio
plt.scatter(
    best_portfolio["Risk"],
    best_portfolio["Return"],
    color="red",
    marker="*",
    s=300,
    label="Maximum Sharpe"
)

# Highlight Minimum Risk Portfolio
plt.scatter(
    lowest_risk_portfolio["Risk"],
    lowest_risk_portfolio["Return"],
    color="blue",
    marker="*",
    s=300,
    label="Minimum Risk"
)

plt.title("Markowitz Efficient Frontier")
plt.xlabel("Portfolio Risk (Volatility)")
plt.ylabel("Expected Annual Return")
plt.legend()
plt.grid(True)

plt.show()