import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Mutual Fund Analytics Dashboard")
st.caption("Bluestock Capstone Project")

# -----------------------------
# Database
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM scheme_performance_clean
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

search = st.sidebar.text_input(
    "🔍 Search Scheme Name"
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

risk = st.sidebar.multiselect(
    "Risk Grade",
    sorted(df["risk_grade"].dropna().unique()),
    default=sorted(df["risk_grade"].dropna().unique())
)

fund_house = st.sidebar.selectbox(
    "Fund House",
    ["All"] + sorted(df["fund_house"].dropna().unique())
)

filtered = df[
    (df["category"].isin(category))
    &
    (df["risk_grade"].isin(risk))
]

if fund_house != "All":
    filtered = filtered[
        filtered["fund_house"] == fund_house
    ]

if search:
    filtered = filtered[
        filtered["scheme_name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Schemes", len(filtered))

c2.metric(
    "Average 3Y Return",
    f"{filtered['return_3yr_pct'].mean():.2f}%"
)

c3.metric(
    "Average Sharpe",
    f"{filtered['sharpe_ratio'].mean():.2f}"
)

c4.metric(
    "Average AUM",
    f"₹ {filtered['aum_crore'].mean():,.0f} Cr"
)

st.divider()

st.subheader("Preview")

st.dataframe(filtered.head(20), use_container_width=True)

st.divider()

st.subheader("📊 Funds by Category")

category_count = (
    filtered["category"]
    .value_counts()
    .reset_index()
)

category_count.columns = ["Category", "Count"]

fig = px.bar(
    category_count,
    x="Category",
    y="Count",
    color="Category",
    title="Number of Funds by Category"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("⭐ Risk Grade Distribution")

risk_count = (
    filtered["risk_grade"]
    .value_counts()
    .reset_index()
)

risk_count.columns = ["Risk Grade", "Count"]

fig = px.pie(
    risk_count,
    names="Risk Grade",
    values="Count",
    hole=0.4,
    title="Funds by Risk Grade"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🏆 Top 10 Funds by 3-Year Return")

top_returns = (
    filtered.sort_values(
        by="return_3yr_pct",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_returns,
    x="return_3yr_pct",
    y="scheme_name",
    color="category",
    orientation="h",
    title="Top 10 Mutual Funds (3-Year Return)"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="3-Year Return (%)",
    yaxis_title="Scheme Name"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("💰 Top 10 Funds by AUM")

top_aum = (
    filtered.sort_values(
        by="aum_crore",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_aum,
    x="aum_crore",
    y="scheme_name",
    color="fund_house",
    orientation="h",
    title="Top 10 Funds by AUM"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="AUM (Crore)",
    yaxis_title="Scheme Name"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📈 Return Comparison (1Y vs 3Y vs 5Y)")

comparison = filtered[
    [
        "scheme_name",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct"
    ]
].head(15)

comparison = comparison.melt(
    id_vars="scheme_name",
    var_name="Return Period",
    value_name="Return (%)"
)

fig = px.bar(
    comparison,
    x="scheme_name",
    y="Return (%)",
    color="Return Period",
    barmode="group",
    title="Return Comparison"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("⭐ Morningstar Rating Distribution")

rating = (
    filtered["morningstar_rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating.columns = ["Rating", "Funds"]

fig = px.bar(
    rating,
    x="Rating",
    y="Funds",
    color="Rating",
    title="Morningstar Ratings"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📉 Alpha vs Sharpe Ratio")

fig = px.scatter(
    filtered,
    x="alpha",
    y="sharpe_ratio",
    color="category",
    hover_name="scheme_name",
    size="aum_crore",
    title="Alpha vs Sharpe Ratio"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📥 Download Data")

csv = filtered.to_csv(index=False)

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_mutual_funds.csv",
    mime="text/csv"
)