# 📈 Mutual Fund Analytics Dashboard

## 📌 Project Overview

This project is a Mutual Fund Analytics Dashboard developed as part of the Bluestock Data Analytics Capstone Project.

The dashboard allows users to analyze mutual fund performance, compare returns, evaluate risk, and generate automated weekly reports using historical NAV data.

---

## 🚀 Features

- Interactive Streamlit Dashboard
- Search Mutual Funds
- Filter by Category
- Filter by Fund House
- Filter by Risk Grade
- KPI Cards
- Top 10 Funds by 3-Year Return
- Top 10 Funds by AUM
- Morningstar Rating Distribution
- Alpha vs Sharpe Ratio Analysis
- Download Filtered Data as CSV
- Automated Weekly HTML Report

---

## 🛠️ Technologies Used

- Python
- Pandas
- SQLite
- Streamlit
- Plotly Express
- NumPy
- Git
- GitHub

---

## 📂 Project Structure

```text
mutual-fund-analytics/
│
├── dashboard/
│   ├── app.py                          # Streamlit Dashboard
│   ├── bluestock_mf_dashboards.pbix    # Power BI Dashboard
│   ├── Dashboard.pdf
│   ├── Page1_IndustryOverview.png
│   ├── Page2_FundPerformance.png
│   ├── Page3_InvestorAnalytics.png
│   ├── Page4_SIPMarketTrends.png
│   └── Page5_NAVDetails.png
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│       └── bluestock_mf.db
│
├── logs/
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── reports/
│   ├── charts/
│   ├── email_reports.py
│   ├── weekly_report.html
│   ├── Final_Report.md
│   ├── Final_Report.pdf
│   └── Presentation.pptx
│
├── scripts/
│   ├── etl_pipeline.py
│   ├── create_sqlite_db.py
│   ├── compute_metrics.py
│   ├── live_nav_fetch.py
│   └── recommender.py
│
├── simulations/
│   ├── monte_carlo_nav.py
│   └── portfolio_optimization.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── requirements.txt
├── .gitignore
└── README.md 
```imulations/

```

---

## ▶️ How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit dashboard

```bash
streamlit run app.py
```

### Generate the Weekly Report

```bash
python reports/email_reports.py
```

---

## 📊 Dashboard Highlights

- Fund Performance Analysis
- Risk Grade Distribution
- Category-wise Analysis
- AUM Comparison
- Return Comparison
- Portfolio Analytics
- Weekly Performance Report

---

## 📄 Project Output

- Interactive Dashboard
- Portfolio Analysis
- HTML Weekly Report
- CSV Download
- SQLite Database

---

## 👨‍💻 Author

**Arunmozhi M**

GitHub: https://github.com/Arunmozhi1997

LinkedIn: https://www.linkedin.com/in/arun-mozhi-65a29037b/

---

## 📜 License

This project was developed for educational purposes as part of the Bluestock Capstone Project.
