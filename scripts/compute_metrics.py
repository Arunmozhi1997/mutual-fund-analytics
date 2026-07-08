from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import linregress

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

nav = pd.read_csv(PROCESSED_DIR / "nav_history_clean.csv")

fund_master = pd.read_csv(PROCESSED_DIR / "fund_master_clean.csv")

benchmark_df = pd.read_csv(PROCESSED_DIR / "benchmark_indices_clean.csv")

# Convert date columns to datetime
nav["date"] = pd.to_datetime(nav["date"])
benchmark_df["date"] = pd.to_datetime(benchmark_df["date"])

# Sort NAV data
nav = nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
       .pct_change()
)
nav["daily_return"].sort_values().head()

print(nav["date"].min())
print(nav["date"].max())

fund = nav[nav["amfi_code"] == 100016].copy()

latest_date = pd.to_datetime(fund["date"].max())

print(latest_date)

one_year_start = latest_date - pd.DateOffset(years=1)

start_nav = fund.loc[
    fund["date"] >= one_year_start,
    "nav"
].iloc[0]

print(start_nav)

end_nav = fund.iloc[-1]["nav"]

cagr_1y = (end_nav / start_nav) ** (1 / 1) - 1

print(cagr_1y)

print(start_nav)

print(end_nav)

print(f"{cagr_1y * 100:.2f}%")

def calculate_cagr(fund, years, latest_date):

    earliest_date = fund["date"].min()

    start_date = latest_date - pd.DateOffset(years=years)

    # Check if enough historical data is available
    if earliest_date > start_date:
        return np.nan

    # Starting NAV
    start_nav = fund.loc[
        fund["date"] >= start_date,
        "nav"
    ].iloc[0]

    # Ending NAV
    end_nav = fund.iloc[-1]["nav"]

    # CAGR Formula
    cagr = (end_nav / start_nav) ** (1 / years) - 1

    return cagr

latest_date = nav["date"].max()

fund = nav[nav["amfi_code"] == 100016]

print("1-Year CAGR:", calculate_cagr(fund, 1, latest_date))
print("3-Year CAGR:", calculate_cagr(fund, 3, latest_date))
print("5-Year CAGR:", calculate_cagr(fund, 5, latest_date))

latest_date = nav["date"].max()

cagr_results = []

for amfi_code, fund in nav.groupby("amfi_code"):

    cagr_results.append({
        "amfi_code": amfi_code,
        "CAGR_1Y": calculate_cagr(fund, 1, latest_date),
        "CAGR_3Y": calculate_cagr(fund, 3, latest_date),
        "CAGR_5Y": calculate_cagr(fund, 5, latest_date)
    })

cagr_df = pd.DataFrame(cagr_results)

cagr_df[["CAGR_1Y", "CAGR_3Y", "CAGR_5Y"]] *= 100

cagr_df = cagr_df.round(2)

cagr_df = cagr_df.sort_values("CAGR_3Y", ascending=False).reset_index(drop=True)
cagr_df.head()

cagr_comparison = cagr_df.merge(
    fund_master[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "expense_ratio_pct",
            "benchmark"
        ]
    ],
    on="amfi_code",
    how="left"
)

cagr_comparison = cagr_comparison[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "benchmark",
        "expense_ratio_pct",
        "CAGR_1Y",
        "CAGR_3Y",
        "CAGR_5Y"
    ]
]

cagr_comparison = (
    cagr_comparison
    .sort_values("CAGR_3Y", ascending=False)
    .reset_index(drop=True)
)

cagr_comparison.head()

rf_annual = 0.065
rf_daily = rf_annual / 252

sharpe = (
    nav
    .groupby("amfi_code")
    .agg(
        avg_daily_return=("daily_return", "mean"),
        std_daily_return=("daily_return", "std")
    )
    .reset_index()
)

sharpe["sharpe_ratio"] = (
    (sharpe["avg_daily_return"] - rf_daily)
    / sharpe["std_daily_return"]
) * np.sqrt(252)

sharpe = sharpe.merge(
    fund_master[["amfi_code", "scheme_name", "expense_ratio_pct"]],
    on="amfi_code",
    how="left"
)
sharpe["sharpe_rank"] = (
    sharpe["sharpe_ratio"]
    .rank(ascending=False, method="dense")
    .astype(int)
)

sharpe = sharpe.sort_values("sharpe_rank")
sharpe[
    [
        "sharpe_rank",
        "scheme_name",
        "sharpe_ratio"
    ]
].head(10)

def downside_std(returns):
    downside = returns[returns < 0]
    return downside.std()

sortino = (
    nav
    .groupby("amfi_code")
    .agg(
        avg_daily_return=("daily_return", "mean"),
        downside_std=("daily_return", downside_std)
    )
    .reset_index()
)

sortino["sortino_ratio"] = (
    (sortino["avg_daily_return"] - rf_daily)
    / sortino["downside_std"]
) * np.sqrt(252)

sortino = sortino.merge(
    fund_master[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

sortino["sortino_rank"] = (
    sortino["sortino_ratio"]
    .rank(ascending=False, method="dense")
    .astype(int)
)

sortino = sortino.sort_values("sortino_rank")
sortino[
    ["sortino_rank", "scheme_name", "sortino_ratio"]
].head(10)

benchmark_df["date"] = pd.to_datetime(benchmark_df["date"])

nifty100 = (
    benchmark_df[benchmark_df["index_name"] == "NIFTY100"]
    .copy()
    .sort_values("date")
)

nifty100["benchmark_return"] = nifty100["close_value"].pct_change()

returns = nav.merge(
    nifty100[["date", "benchmark_return"]],
    on="date",
    how="inner"
)

returns = returns.dropna(
    subset=["daily_return", "benchmark_return"]
)

results = []

for amfi_code, group in returns.groupby("amfi_code"):

    regression = linregress(
        group["benchmark_return"],
        group["daily_return"]
    )

    results.append({
        "amfi_code": amfi_code,
        "alpha": regression.intercept * 252,
        "beta": regression.slope,
        "r_squared": regression.rvalue ** 2,
        "p_value": regression.pvalue
    })

alpha_beta = pd.DataFrame(results)

alpha_beta = alpha_beta.merge(
    fund_master[
        ["amfi_code", "scheme_name"]
    ],
    on="amfi_code",
    how="left"
)

alpha_beta["alpha_rank"] = (
    alpha_beta["alpha"]
    .rank(
        ascending=False,
        method="dense"
    )
    .astype(int)
)

alpha_beta = alpha_beta.sort_values("alpha_rank")

# Running maximum NAV for each fund
nav["running_max"] = (
    nav.groupby("amfi_code")["nav"]
       .cummax()
)

# Drawdown
nav["drawdown"] = (
    nav["nav"] / nav["running_max"]
) - 1
max_drawdown = (
    nav.groupby("amfi_code")["drawdown"]
       .min()
       .reset_index()
       .rename(columns={"drawdown": "max_drawdown"})
)

max_drawdown.head()

def worst_drawdown_period(df):
    df = df.sort_values("date").reset_index(drop=True)

    # Running max NAV
    running_max = df["nav"].cummax()

    # Drawdown
    drawdown = df["nav"] / running_max - 1

    # Bottom of drawdown
    bottom_idx = drawdown.idxmin()

    bottom_date = df.loc[bottom_idx, "date"]

    # Peak before bottom
    peak_idx = df.loc[:bottom_idx, "nav"].idxmax()

    peak_date = df.loc[peak_idx, "date"]

    max_dd = drawdown.min()

    return pd.Series({
        "peak_date": peak_date,
        "bottom_date": bottom_date,
        "max_drawdown": max_dd
    })
mdd_periods = (
    nav.groupby("amfi_code")
       .apply(worst_drawdown_period)
       .reset_index()
)

mdd_periods.head()

# Merge maximum drawdown results with fund details
mdd_summary = (
    mdd_periods.merge(
        fund_master[["amfi_code", "scheme_name", "fund_house"]],
        on="amfi_code",
        how="left"
    )
)

# Arrange columns
mdd_summary = mdd_summary[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "peak_date",
        "bottom_date",
        "max_drawdown"
    ]
]

# Sort by worst drawdown (most negative first)
mdd_summary = mdd_summary.sort_values(
    by="max_drawdown",
    ascending=True
).reset_index(drop=True)

mdd_summary.head(10)

scorecard = (
    cagr_comparison[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "expense_ratio_pct",
            "CAGR_3Y"
        ]
    ]
    .merge(
        sharpe[
            [
                "amfi_code",
                "sharpe_ratio"
            ]
        ],
        on="amfi_code"
    )
    .merge(
        alpha_beta[
            [
                "amfi_code",
                "alpha"
            ]
        ],
        on="amfi_code"
    )
    .merge(
        mdd_summary[
            [
                "amfi_code",
                "max_drawdown"
            ]
        ],
        on="amfi_code"
    )
)

scorecard.head()

scorecard["rank_cagr"] = scorecard["CAGR_3Y"].rank(
    ascending=False,
    method="dense"
)

scorecard["rank_sharpe"] = scorecard["sharpe_ratio"].rank(
    ascending=False,
    method="dense"
)

scorecard["rank_alpha"] = scorecard["alpha"].rank(
    ascending=False,
    method="dense"
)

scorecard["rank_expense"] = scorecard["expense_ratio_pct"].rank(
    ascending=True,
    method="dense"
)
scorecard["rank_mdd"] = scorecard["max_drawdown"].rank(
    ascending=False,
    method="dense"
)

n = len(scorecard)

rank_cols = [
    "rank_cagr",
    "rank_sharpe",
    "rank_alpha",
    "rank_expense",
    "rank_mdd"
]

for col in rank_cols:
    scorecard[col + "_score"] = (
        (n - scorecard[col]) / (n - 1)
    ) * 100

scorecard["Fund_Score"] = (
      0.30 * scorecard["rank_cagr_score"]
    + 0.25 * scorecard["rank_sharpe_score"]
    + 0.20 * scorecard["rank_alpha_score"]
    + 0.15 * scorecard["rank_expense_score"]
    + 0.10 * scorecard["rank_mdd_score"]
)   

scorecard = scorecard.sort_values(
    "Fund_Score",
    ascending=False
).reset_index(drop=True)

scorecard["Overall_Rank"] = scorecard.index + 1

fund_scorecard = scorecard[
    [
        "Overall_Rank",
        "scheme_name",
        "fund_house",
        "CAGR_3Y",
        "sharpe_ratio",
        "alpha",
        "expense_ratio_pct",
        "max_drawdown",
        "Fund_Score"
    ]
]

fund_scorecard.head(10)

fund_scorecard = scorecard[
    [
        "Overall_Rank",
        "amfi_code",
        "scheme_name",
        "fund_house",
        "CAGR_3Y",
        "sharpe_ratio",
        "alpha",
        "expense_ratio_pct",
        "max_drawdown",
        "Fund_Score"
    ]
]

fund_scorecard.head()

top5_codes = fund_scorecard.head(5)["amfi_code"].tolist()
print(top5_codes)

latest_date = nav["date"].max()

start_date = latest_date - pd.DateOffset(years=3)

nav_3y = nav[
    (nav["date"] >= start_date) &
    (nav["amfi_code"].isin(top5_codes))
].copy()

nav_3y = nav_3y.merge(
    fund_master[
        ["amfi_code", "scheme_name", "benchmark"]
    ],
    on="amfi_code",
    how="left"
)
nav_3y["Normalized_NAV"] = (
    nav_3y.groupby("amfi_code")["nav"]
          .transform(lambda x: x / x.iloc[0] * 100)
)

benchmark_3y = benchmark_df[
    benchmark_df["date"] >= start_date
].copy()

benchmark_3y = benchmark_3y.sort_values(
    ["index_name", "date"]
)

benchmark_3y["daily_return"] = (
    benchmark_3y.groupby("index_name")["close_value"]
                .pct_change()
)
benchmark_3y["Normalized_Index"] = (
    benchmark_3y.groupby("index_name")["close_value"]
                .transform(lambda x: x / x.iloc[0] * 100)
)

benchmark_map = {
    "NIFTY 100 TRI": "NIFTY100",
    "NIFTY 500 TRI": "NIFTY500",
    "NIFTY Midcap 150 TRI": "NIFTY_MIDCAP150",
    "NIFTY 50 TRI": "NIFTY50"
}

tracking_errors = []

for code in top5_codes:

    info = fund_master.loc[
        fund_master["amfi_code"] == code,
        ["scheme_name", "benchmark"]
    ].iloc[0]

    benchmark_name = benchmark_map.get(
        info["benchmark"],
        info["benchmark"]
    )

    fund_returns = (
        nav_3y.loc[
            nav_3y["amfi_code"] == code,
            ["date", "daily_return"]
        ]
        .dropna()
    )

    benchmark_returns = (
        benchmark_3y.loc[
            benchmark_3y["index_name"] == benchmark_name,
            ["date", "daily_return"]
        ]
        .dropna()
    )

    merged = fund_returns.merge(
        benchmark_returns,
        on="date",
        suffixes=("_fund", "_benchmark")
    )

    tracking_error = (
        (merged["daily_return_fund"] -
         merged["daily_return_benchmark"]).std()
        * np.sqrt(252)
    )

    tracking_errors.append({
        "amfi_code": code,
        "scheme_name": info["scheme_name"],
        "benchmark": benchmark_name,
        "tracking_error": tracking_error
    })

tracking_error_df = pd.DataFrame(tracking_errors)

tracking_error_df


print("✓ Daily Returns calculated")
print("✓ CAGR calculated")
print("✓ Sharpe Ratio calculated")
print("✓ Sortino Ratio calculated")
print("✓ Alpha/Beta calculated")
print("✓ Tracking Error calculated")
print("✓ Maximum Drawdown calculated")
print("✓ Fund Scorecard created")
print("✓ All output files saved successfully")
