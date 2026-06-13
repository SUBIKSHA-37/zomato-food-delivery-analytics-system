import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import os
 
# ─────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────
DB_CONFIG = {
    "user":     "root",
    "password": "yourpassword",
    "host":     "localhost",
    "port":     3306,
    "database": "zomatoapp",
}
 
# Build SQLAlchemy engine (connection string)
DB_URI = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
 
engine = create_engine(DB_URI, echo=False)
 
# Output directories
OUTPUT_DIR   = "etl_output/csv"
ANALYTICS_DB = "zomatoapp"        # Same DB, analytics tables
 
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# ─────────────────────────────────────────────────────────
# STEP 1 — EXTRACT
# ─────────────────────────────────────────────────────────
print("\n" + "="*50)
print("STEP 1: EXTRACTING DATA FROM MYSQL")
print("="*50)
 
def extract_all():
    """Extract all raw tables from MySQL into DataFrames"""
    with engine.connect() as conn:
        customers = pd.read_sql("SELECT * FROM customers", conn)
        foods     = pd.read_sql("SELECT * FROM foods", conn)
        orders    = pd.read_sql("SELECT * FROM orders", conn)
        items     = pd.read_sql("SELECT * FROM order_items", conn)
        delivery  = pd.read_sql("SELECT * FROM delivery_details", conn)
 
    print(f"  ✔ customers   : {len(customers)} rows")
    print(f"  ✔ foods       : {len(foods)} rows")
    print(f"  ✔ orders      : {len(orders)} rows")
    print(f"  ✔ order_items : {len(items)} rows")
    print(f"  ✔ delivery    : {len(delivery)} rows")
 
    return customers, foods, orders, items, delivery
 
customers_raw, foods_raw, orders_raw, items_raw, delivery_raw = extract_all()
 
 
# ─────────────────────────────────────────────────────────
# STEP 2 — TRANSFORM
# ─────────────────────────────────────────────────────────
print("\n" + "="*50)
print("STEP 2: TRANSFORMING DATA")
print("="*50)
 
 
# ── 2a. Clean customers ──────────────────────────────────
def transform_customers(df):
    df = df.copy()
    df.drop_duplicates(subset=["email"], inplace=True)          
    df.dropna(subset=["name", "email"], inplace=True)           
    df["mobile"]     = df["mobile"].fillna("Unknown")           
    df["created_at"] = pd.to_datetime(df["created_at"])        
    df["month_joined"] = df["created_at"].dt.month_name()
    df.drop(columns=["password_hash"], errors="ignore", inplace=True)  
    print(f"  ✔ Customers cleaned: {len(df)} records")
    return df
 
customers_clean = transform_customers(customers_raw)
 
 
# ── 2b. Clean foods ──────────────────────────────────────
def transform_foods(df):
    df = df.copy()
    df.dropna(subset=["food_name", "category", "price"], inplace=True)
    df["price"]  = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
    df["price_tier"] = pd.cut(
        df["price"],
        bins=[0, 150, 250, 350, float("inf")],
        labels=["Budget", "Mid-range", "Premium", "Luxury"]
    )
    print(f"  ✔ Foods cleaned: {len(df)} records")
    return df
 
foods_clean = transform_foods(foods_raw)
 
 
# ── 2c. Clean orders ─────────────────────────────────────
def transform_orders(df):
    df = df.copy()
    df.dropna(subset=["customer_id", "total_amount"], inplace=True)
    df["order_date"]    = pd.to_datetime(df["order_date"])
    df["order_year"]    = df["order_date"].dt.year
    df["order_month"]   = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.month_name()
    df["order_day_name"]   = df["order_date"].dt.day_name()
    df["order_hour"]       = df["order_date"].dt.hour
 
    # Tag time of day
    df["time_of_day"] = pd.cut(
        df["order_hour"],
        bins=[-1, 11, 14, 17, 21, 24],
        labels=["Morning", "Lunch", "Afternoon", "Dinner", "Late Night"]
    )
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
    print(f"  ✔ Orders cleaned: {len(df)} records")
    return df
 
orders_clean = transform_orders(orders_raw)
 
 
# ── 2d. Build revenue metrics ────────────────────────────
def build_revenue_metrics(orders_df, items_df, foods_df):
    """Create rich analytics fact table"""
 
    # Merge items → foods → orders
    merged = (
        items_df
        .merge(foods_df[["food_id", "food_name", "category", "restaurant_name"]], on="food_id")
        .merge(orders_df[["order_id", "customer_id", "order_date", "order_month_name",
                           "order_year", "time_of_day"]], on="order_id")
    )
    merged["line_total"] = merged["quantity"] * merged["price"]
 
    print(f"  ✔ Revenue fact table: {len(merged)} rows")
    return merged
 
revenue_fact = build_revenue_metrics(
    orders_clean, items_raw, foods_clean
)
 
 
# ── 2e. Compute summary metrics ──────────────────────────
def compute_kpis(orders_df, revenue_df, customers_df):
    total_revenue   = revenue_df["line_total"].sum()
    total_orders    = orders_df["order_id"].nunique()
    total_customers = customers_df["customer_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0
 
    kpi = pd.DataFrame([{
        "metric": "Total Revenue (₹)",      "value": round(total_revenue, 2)},
        {"metric": "Total Orders",          "value": total_orders},
        {"metric": "Total Customers",       "value": total_customers},
        {"metric": "Avg Order Value (₹)",   "value": round(avg_order_value, 2)},
        {"metric": "ETL Run Timestamp",     "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ])
    print("  ✔ KPI summary computed")
    print(kpi.to_string(index=False))
    return kpi
 
kpi_df = compute_kpis(orders_clean, revenue_fact, customers_clean)
 
 
# ── 2f. Category-level aggregation ──────────────────────
def category_revenue(revenue_df):
    cat = (
        revenue_df
        .groupby("category")
        .agg(
            total_revenue=("line_total",  "sum"),
            total_orders =("order_id",    "nunique"),
            total_items  =("quantity",    "sum"),
            avg_price    =("price",       "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    cat["revenue_share_%"] = (cat["total_revenue"] / cat["total_revenue"].sum() * 100).round(2)
    print(f"  ✔ Category revenue: {len(cat)} categories")
    return cat
 
category_df = category_revenue(revenue_fact)
 
 
# ── 2g. Monthly revenue trend ───────────────────────────
def monthly_revenue(revenue_df):
    monthly = (
        revenue_df
        .groupby(["order_year", "order_month_name"])
        .agg(
            revenue=("line_total", "sum"),
            orders =("order_id",   "nunique"),
        )
        .reset_index()
        .sort_values(["order_year", "revenue"], ascending=[True, False])
    )
    print(f"  ✔ Monthly revenue: {len(monthly)} months")
    return monthly
 
monthly_df = monthly_revenue(revenue_fact)
 
 
# ── 2h. Top selling foods ────────────────────────────────
def top_foods(revenue_df, top_n=10):
    foods = (
        revenue_df
        .groupby(["food_id", "food_name", "category"])
        .agg(
            total_qty    =("quantity",  "sum"),
            total_revenue=("line_total","sum"),
            order_count  =("order_id",  "nunique"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
        .head(top_n)
    )
    print(f"  ✔ Top {top_n} foods computed")
    return foods
 
top_foods_df = top_foods(revenue_fact)
 
 
# ── 2i. Customer insights ────────────────────────────────
def customer_insights(orders_df, revenue_df, customers_df):
    cust_stats = (
        revenue_df
        .groupby("customer_id")
        .agg(
            total_spent  =("line_total","sum"),
            total_orders =("order_id",  "nunique"),
            total_items  =("quantity",  "sum"),
        )
        .reset_index()
    )
    cust_stats["avg_order_value"] = (cust_stats["total_spent"] / cust_stats["total_orders"]).round(2)
    cust_stats["is_repeat"]       = cust_stats["total_orders"] > 1
 
    # Merge customer names
    cust_stats = cust_stats.merge(
        customers_df[["customer_id", "name", "email"]], on="customer_id"
    ).sort_values("total_spent", ascending=False)
 
    print(f"  ✔ Customer insights: {len(cust_stats)} customers")
    return cust_stats
 
customer_df = customer_insights(orders_clean, revenue_fact, customers_clean)
 
 
# ─────────────────────────────────────────────────────────
# STEP 3 — LOAD
# ─────────────────────────────────────────────────────────
print("\n" + "="*50)
print("STEP 3: LOADING DATA")
print("="*50)
 
 
# ── 3a. Save to CSV ──────────────────────────────────────
def save_csv(df, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    print(f"  ✔ Saved CSV: {path}")
 
save_csv(customers_clean, "customers_clean.csv")
save_csv(foods_clean,     "foods_clean.csv")
save_csv(orders_clean,    "orders_clean.csv")
save_csv(revenue_fact,    "revenue_fact.csv")
save_csv(category_df,     "category_revenue.csv")
save_csv(monthly_df,      "monthly_revenue.csv")
save_csv(top_foods_df,    "top_foods.csv")
save_csv(customer_df,     "customer_insights.csv")
save_csv(kpi_df,          "kpi_summary.csv")
 
 
# ── 3b. Load analytics tables back into MySQL ────────────
def load_to_db(df, table_name, if_exists="replace"):
    """Write DataFrame to MySQL analytics table"""
    df.to_sql(
        table_name,
        con=engine,
        if_exists=if_exists,   # 'replace' drops & recreates; 'append' adds rows
        index=False,
        method="multi",        # Batch insert for speed
        chunksize=500,
    )
    print(f"  ✔ Loaded to DB table: {table_name} ({len(df)} rows)")
 
load_to_db(revenue_fact,  "analytics_revenue_fact")
load_to_db(category_df,   "analytics_category_revenue")
load_to_db(monthly_df,    "analytics_monthly_revenue")
load_to_db(top_foods_df,  "analytics_top_foods")
load_to_db(customer_df,   "analytics_customer_insights")
load_to_db(kpi_df,        "analytics_kpi_summary")
 
 
print("\n" + "="*50)
print("✅ ETL PIPELINE COMPLETE!")
print("="*50)
print(f"  CSVs saved to  : {OUTPUT_DIR}/")
print(f"  DB tables in   : analytics_* tables in {ANALYTICS_DB}")
 

