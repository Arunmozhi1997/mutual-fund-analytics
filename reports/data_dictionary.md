# Data Dictionary

## dim_fund

| Column | Data Type | Description |
|----------|----------|-------------|
| amfi_code | BIGINT | Unique mutual fund identifier |
| fund_house | VARCHAR(255) | Asset Management Company |
| scheme_name | TEXT | Mutual fund scheme name |
| category | VARCHAR(100) | Fund category |
| sub_category | VARCHAR(100) | Fund sub-category |
| plan | VARCHAR(50) | Direct or Regular plan |
| launch_date | DATE | Fund launch date |
| benchmark | TEXT | Benchmark index |
| expense_ratio_pct | NUMERIC(5,2) | Expense ratio percentage |
| exit_load_pct | NUMERIC(5,2) | Exit load percentage |
| min_sip_amount | NUMERIC(12,2) | Minimum SIP investment |
| min_lumpsum_amount | NUMERIC(12,2) | Minimum lump sum investment |
| fund_manager | VARCHAR(255) | Fund manager name |
| risk_category | VARCHAR(50) | Risk classification |
| sebi_category_code | VARCHAR(50) | SEBI category code |

Source: fund_master_clean.csv

---

## fact_nav

| Column | Data Type | Description |
|----------|----------|-------------|
| amfi_code | BIGINT | Mutual fund identifier |
| date | DATE | NAV date |
| nav | NUMERIC(12,4) | Net Asset Value |

Source: nav_history_clean.csv

---

## fact_transactions

| Column | Data Type | Description |
|----------|----------|-------------|
| investor_id | VARCHAR(50) | Investor identifier |
| transaction_date | DATE | Transaction date |
| amfi_code | BIGINT | Mutual fund identifier |
| transaction_type | VARCHAR(50) | SIP, Lumpsum, Redemption |
| amount_inr | NUMERIC(15,2) | Transaction amount |
| state | VARCHAR(100) | Investor state |
| city | VARCHAR(100) | Investor city |
| city_tier | VARCHAR(20) | Tier classification |
| age_group | VARCHAR(20) | Investor age category |
| gender | VARCHAR(20) | Investor gender |
| annual_income_lakh | NUMERIC(10,2) | Annual income in lakhs |
| payment_mode | VARCHAR(50) | Payment method |
| kyc_status | VARCHAR(20) | KYC verification status |

Source: investor_transactions_clean.csv

---

## fact_performance

| Column | Data Type | Description |
|----------|----------|-------------|
| amfi_code | BIGINT | Mutual fund identifier |
| scheme_name | TEXT | Mutual fund scheme |
| fund_house | VARCHAR(255) | Fund house |
| category | VARCHAR(100) | Fund category |
| plan | VARCHAR(50) | Plan type |
| return_1yr_pct | NUMERIC(8,2) | One-year return |
| return_3yr_pct | NUMERIC(8,2) | Three-year return |
| return_5yr_pct | NUMERIC(8,2) | Five-year return |
| benchmark_3yr_pct | NUMERIC(8,2) | Benchmark return |
| alpha | NUMERIC(8,2) | Alpha measure |
| beta | NUMERIC(8,2) | Beta measure |
| sharpe_ratio | NUMERIC(8,2) | Risk-adjusted return |
| sortino_ratio | NUMERIC(8,2) | Downside risk-adjusted return |
| std_dev_ann_pct | NUMERIC(8,2) | Annualized volatility |
| max_drawdown_pct | NUMERIC(8,2) | Maximum drawdown |
| aum_crore | NUMERIC(18,2) | Assets Under Management |
| expense_ratio_pct | NUMERIC(5,2) | Expense ratio |
| morningstar_rating | INTEGER | Morningstar rating |
| risk_grade | VARCHAR(20) | Risk grade |
| anomaly_flag | BOOLEAN | Data anomaly indicator |

Source: scheme_performance_clean.csv