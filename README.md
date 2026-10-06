# 🎧 boAt Sales Analytics — End-to-End Data Analysis Project

<p align="center">
  <img src="dashboard/Screenshot 2026-08-03 145810.png" alt="boAt Sales Analytics Dashboard" width="900"/>
</p>

> **A complete data analytics case study** covering Python data cleaning, SQL analysis, and Power BI dashboard visualization — built on a simulated boAt Lifestyle sales dataset of **10,000 orders**.

---

## 📌 Project Overview

This project demonstrates a full-cycle analytics workflow on a **boAt (consumer electronics)** sales dataset. Starting from data  cleaning progresses to SQL-based analysis, and culminates in an interactive **Power BI dashboard** with business insights and recommendations.

| KPI | Value |
|-----|-------|
| **Total Revenue** | ₹21.84M |
| **Total Profit** | ₹10.42M |
| **Total Orders** | 10,000 |
| **Avg Rating** | 4.33 ⭐ |
| **Profit Margin** | 47.7% |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Pandas** | Data Cleaning & transformation |
| **SQLite** | SQL-based exploratory analysis |
| **Power BI** | Interactive dashboard & DAX measures |

---

## 📂 Project Structure

```
boat/
│
├── data_cleaning.py                    # Cleans & enriches data (adds Profit Margin, Quarter, etc.)
├── sql_analysis.py                     # SQL queries mirroring every Power BI visual
│
├── boAt_Case_Study.md                  # Detailed analytical case study (markdown)
├── boAt_Professional_Report (1).pdf    # Professional report (PDF)
├── POWERBI_STEP_BY_STEP.md             # Step-by-step Power BI dashboard build guide
│
├── boAt.pbix                           # Power BI dashboard file
│
├── dashboard/                          # Dashboard screenshot
│   └── Screenshot.png
│
└── README.md
```

---

## 📊 Dashboard Highlights

The Power BI dashboard features a **dark-themed, interactive** layout with:

- **5 KPI Cards** — Revenue, Profit, Orders, Avg Rating, Avg Selling Price
- **3 Slicers** — Filter by State, Sales Channel, Product Category
- **Map Visual** — State-wise performance across 35 Indian states
- **Donut Charts** — Sales by Age Group & Payment Mode breakdown
- **Bar Charts** — Revenue by Sales Channel, Top 5 Products, Top 5 Cities
- **Line Chart** — Monthly revenue trend with seasonal patterns

---

## 🔄 Workflow

```

Data Cleaning (Pandas)
        ↓
SQL Analysis (SQLite)
        ↓
Data Validation
        ↓
Power BI Import → DAX Measures → Dashboard → Insights
```

---

## 💡 Key Insights

1. **Festival Season Dominance** — Oct–Nov drove **₹5.12M** combined revenue (~23% of annual), fuelled by Diwali and e-commerce sales events
2. **Online Channels Lead** — Amazon (₹4.54M) and Flipkart (₹4.15M) together account for **61%+** of total revenue
3. **Earbuds = Volume Leader** — 3,001 orders, nearly 2× the next category (Neckbands)
4. **Smartwatches = Revenue King** — Highest per-order revenue despite lower volume
5. **26–35 Age Group** — The largest customer segment, driving maximum sales contribution
6. **South & West Regions** — Maharashtra, Karnataka, Tamil Nadu are the top revenue states

---

## 🚀 How to Run

### 1. Clean Data
```bash
python data_cleaning.py
```
> Produces `boat_sales_cleaned.csv` — ready for Power BI import

### 2. Run SQL Analysis
```bash
python sql_analysis.py
```
> Loads data into SQLite and runs all dashboard-matching queries

### 3. Open Power BI Dashboard
> Open `boAt.pbix` in Power BI Desktop and connect to `boat_sales_cleaned.csv`

---



---

## 📁 Dataset Details

| Attribute | Detail |
|-----------|--------|
| Total Records | 10,000 orders |
| Time Period | January – December 2024 |
| Products | 37 real boAt products |
| Categories | 6 (Earbuds, Headphones, Neckband, Smartwatch, Speaker, Wired Earphones) |
| States | 35 Indian states/UTs |
| Cities | 139 cities |
| Columns | 27 attributes |

---


