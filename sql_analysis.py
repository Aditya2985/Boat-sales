"""
============================================================
 boAt Sales Analytics - SQL Analysis Script
============================================================
 This script loads the CSV into SQLite and runs SQL queries
 that mirror every visual in the Power BI dashboard.
 Use these queries to verify your Power BI DAX measures.
============================================================
"""

import sqlite3
import pandas as pd
import os

# ─────────────────── LOAD DATA ───────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "boat_sales.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "boat_sales_data.csv")

def create_database():
    """Load CSV into SQLite database."""
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.commit()
    print(f"[OK] Loaded {len(df):,} rows into SQLite database: {DB_PATH}")
    return conn


def run_query(conn, title, query):
    """Run a SQL query and print results."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    print()
    return result


# ─────────────────── SQL QUERIES (match each dashboard visual) ───────────────────

def run_all_analyses(conn):
    """Run all SQL queries matching the Power BI dashboard visuals."""

    # ━━━━━━━━━━━━━━━ KPI CARDS (Top Row) ━━━━━━━━━━━━━━━
    run_query(conn, "KPI CARDS - Overall Metrics", """
        SELECT
            COUNT(*)                          AS Total_Orders,
            ROUND(SUM(Revenue), 2)            AS Total_Revenue,
            ROUND(SUM(Profit), 2)             AS Total_Profit,
            ROUND(AVG(Rating), 2)             AS Avg_Rating,
            ROUND(AVG(Quantity), 2)           AS Avg_Sales,
            ROUND(SUM(Profit)*100.0/SUM(Revenue), 1) AS Profit_Margin_Pct
        FROM sales
    """)

    # ━━━━━━━━━━━━━━━ SALES BY AGE GROUP (Donut Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "SALES BY AGE GROUP (Donut Chart)", """
        SELECT
            Age_Group,
            COUNT(*)                                    AS Order_Count,
            ROUND(COUNT(*)*100.0 / (SELECT COUNT(*) FROM sales), 1) AS Pct
        FROM sales
        GROUP BY Age_Group
        ORDER BY Order_Count DESC
    """)

    # ━━━━━━━━━━━━━━━ PAYMENT MODES (Donut Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "PAYMENT MODES (Donut Chart)", """
        SELECT
            Payment_Mode,
            COUNT(*)                                    AS Order_Count,
            ROUND(COUNT(*)*100.0 / (SELECT COUNT(*) FROM sales), 2) AS Pct
        FROM sales
        GROUP BY Payment_Mode
        ORDER BY Order_Count DESC
    """)

    # ━━━━━━━━━━━━━━━ REVENUE BY SALES CHANNELS (Bar Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "REVENUE BY SALES CHANNELS (Bar Chart)", """
        SELECT
            Sales_Channel,
            COUNT(*)                    AS Order_Count,
            ROUND(SUM(Revenue), 0)      AS Total_Revenue,
            ROUND(SUM(Profit), 0)       AS Total_Profit,
            ROUND(AVG(Rating), 2)       AS Avg_Rating
        FROM sales
        GROUP BY Sales_Channel
        ORDER BY Total_Revenue DESC
    """)

    # ━━━━━━━━━━━━━━━ REVENUE TREND BY MONTH (Line Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "REVENUE TREND BY MONTH (Line Chart)", """
        SELECT
            Month,
            Month_Num,
            COUNT(*)                    AS Orders,
            ROUND(SUM(Revenue), 0)      AS Revenue,
            ROUND(SUM(Profit), 0)       AS Profit
        FROM sales
        GROUP BY Month, Month_Num
        ORDER BY Month_Num
    """)

    # ━━━━━━━━━━━━━━━ TOP 5 PRODUCTS BY SALES (Bar Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "TOP 5 PRODUCTS BY SALES (Horizontal Bar)", """
        SELECT
            Product_Name,
            COUNT(*)                    AS Total_Sales,
            ROUND(SUM(Revenue), 0)      AS Total_Revenue
        FROM sales
        GROUP BY Product_Name
        ORDER BY Total_Sales DESC
        LIMIT 5
    """)

    # ━━━━━━━━━━━━━━━ TOP 5 CITIES BY SALES (Bar Chart) ━━━━━━━━━━━━━━━
    run_query(conn, "TOP 5 CITIES BY SALES (Horizontal Bar)", """
        SELECT
            City,
            State,
            COUNT(*)                    AS Total_Sales,
            ROUND(SUM(Revenue), 0)      AS Total_Revenue
        FROM sales
        GROUP BY City, State
        ORDER BY Total_Sales DESC
        LIMIT 5
    """)

    # ━━━━━━━━━━━━━━━ STATE-WISE PERFORMANCE (Map Visual) ━━━━━━━━━━━━━━━
    run_query(conn, "STATE-WISE PERFORMANCE (Top 10 by Revenue)", """
        SELECT
            State,
            Region,
            COUNT(*)                    AS Orders,
            ROUND(SUM(Revenue), 0)      AS Revenue,
            ROUND(SUM(Profit), 0)       AS Profit,
            ROUND(AVG(Rating), 2)       AS Avg_Rating
        FROM sales
        GROUP BY State, Region
        ORDER BY Revenue DESC
        LIMIT 10
    """)

    # ━━━━━━━━━━━━━━━ CATEGORY BREAKDOWN ━━━━━━━━━━━━━━━
    run_query(conn, "CATEGORY BREAKDOWN", """
        SELECT
            Category,
            COUNT(*)                    AS Orders,
            ROUND(SUM(Revenue), 0)      AS Revenue,
            ROUND(SUM(Profit), 0)       AS Profit,
            ROUND(AVG(Rating), 2)       AS Avg_Rating,
            ROUND(AVG(Selling_Price), 0) AS Avg_Selling_Price
        FROM sales
        GROUP BY Category
        ORDER BY Revenue DESC
    """)

    # ━━━━━━━━━━━━━━━ GENDER DISTRIBUTION ━━━━━━━━━━━━━━━
    run_query(conn, "GENDER DISTRIBUTION", """
        SELECT
            Gender,
            COUNT(*)                                    AS Orders,
            ROUND(COUNT(*)*100.0 / (SELECT COUNT(*) FROM sales), 1) AS Pct,
            ROUND(SUM(Revenue), 0)                       AS Revenue
        FROM sales
        GROUP BY Gender
        ORDER BY Orders DESC
    """)

    # ━━━━━━━━━━━━━━━ DISCOUNT ANALYSIS ━━━━━━━━━━━━━━━
    run_query(conn, "DISCOUNT IMPACT ANALYSIS", """
        SELECT
            CASE
                WHEN Discount_Pct BETWEEN 0 AND 10   THEN '0-10%'
                WHEN Discount_Pct BETWEEN 11 AND 20  THEN '11-20%'
                WHEN Discount_Pct BETWEEN 21 AND 30  THEN '21-30%'
                WHEN Discount_Pct BETWEEN 31 AND 40  THEN '31-40%'
                ELSE '40%+'
            END AS Discount_Range,
            COUNT(*)                    AS Orders,
            ROUND(AVG(Selling_Price), 0) AS Avg_Selling_Price,
            ROUND(SUM(Revenue), 0)      AS Total_Revenue,
            ROUND(AVG(Rating), 2)       AS Avg_Rating
        FROM sales
        GROUP BY Discount_Range
        ORDER BY Discount_Range
    """)

    # ━━━━━━━━━━━━━━━ REGION-WISE SUMMARY ━━━━━━━━━━━━━━━
    run_query(conn, "REGION-WISE SUMMARY", """
        SELECT
            Region,
            COUNT(DISTINCT State)       AS States,
            COUNT(DISTINCT City)        AS Cities,
            COUNT(*)                    AS Orders,
            ROUND(SUM(Revenue), 0)      AS Revenue,
            ROUND(SUM(Profit), 0)       AS Profit
        FROM sales
        GROUP BY Region
        ORDER BY Revenue DESC
    """)


# ─────────────────── MAIN ───────────────────

if __name__ == "__main__":
    print("\n  boAt Sales Analytics - SQL Analysis")
    print("  " + "-"*45)
    conn = create_database()
    run_all_analyses(conn)
    conn.close()
    print(f"\n  [OK] All analyses complete. Database: {DB_PATH}\n")
