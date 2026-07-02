CREATE TABLE dim_fund (
    amfi_code BIGINT PRIMARY KEY,
    fund_house VARCHAR(255),
    scheme_name TEXT,
    category VARCHAR(100),
    sub_category VARCHAR(100),
    plan VARCHAR(50),
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct NUMERIC(5,2),
    exit_load_pct NUMERIC(5,2),
    min_sip_amount NUMERIC(12,2),
    min_lumpsum_amount NUMERIC(12,2),
    fund_manager VARCHAR(255),
    risk_category VARCHAR(50),
    sebi_category_code VARCHAR(50)
);

CREATE TABLE fact_nav (
    amfi_code BIGINT,
    date DATE,
    nav NUMERIC(12,4),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
    investor_id VARCHAR(50),
    transaction_date DATE,
    amfi_code BIGINT,
    transaction_type VARCHAR(50),
    amount_inr NUMERIC(15,2),
    state VARCHAR(100),
    city VARCHAR(100),
    city_tier VARCHAR(20),
    age_group VARCHAR(20),
    gender VARCHAR(20),
    annual_income_lakh NUMERIC(10,2),
    payment_mode VARCHAR(50),
    kyc_status VARCHAR(20),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
    amfi_code BIGINT,
    scheme_name TEXT,
    fund_house VARCHAR(255),
    category VARCHAR(100),
    plan VARCHAR(50),
    return_1yr_pct NUMERIC(8,2),
    return_3yr_pct NUMERIC(8,2),
    return_5yr_pct NUMERIC(8,2),
    benchmark_3yr_pct NUMERIC(8,2),
    alpha NUMERIC(8,2),
    beta NUMERIC(8,2),
    sharpe_ratio NUMERIC(8,2),
    sortino_ratio NUMERIC(8,2),
    std_dev_ann_pct NUMERIC(8,2),
    max_drawdown_pct NUMERIC(8,2),
    aum_crore NUMERIC(18,2),
    expense_ratio_pct NUMERIC(5,2),
    morningstar_rating INTEGER,
    risk_grade VARCHAR(20),
    anomaly_flag BOOLEAN,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    day INTEGER,
    day_name VARCHAR(20)
);
CREATE TABLE fact_aum (
    report_date DATE,
    fund_house VARCHAR(255),
    aum_lakh_crore NUMERIC(10,2),
    aum_crore BIGINT,
    num_schemes INTEGER
);