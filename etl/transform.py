import pandas as pd
import os
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE_PATH = os.path.join(BASE_DIR, "data", "superstore.csv")
OUT_FILE_PATH = os.path.join(BASE_DIR, "data", "transformed_superstore.csv")

def transform(df):
    print("Starting data transformation...")

    # Remove duplicate rows (exact duplicates)
    df.drop_duplicates(inplace=True)

    # Convert date columns (coerce errors)
    df["Order.Date"] = pd.to_datetime(df["Order.Date"], errors="coerce")
    df["Ship.Date"] = pd.to_datetime(df["Ship.Date"], errors="coerce")

    # Rename columns for consistency and database compatibility
    df.rename(columns={
        "Order.Date": "order_date",
        "Ship.Date": "ship_date",
        "Order Year": "order_year",
        "Order Month": "order_month",
        "Week": "week",
        "Day of Week": "day_of_week",
        "Processing Time": "processing_time",
        "Profit Margin %": "profit_margin_percent",
        "Sales Category": "sales_category"
    }, inplace=True)

    # Create new time-based features
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["week"] = df["order_date"].dt.isocalendar().week
    df["day_of_week"] = df["order_date"].dt.day_name()

    print(f"Before filtering: {df.shape}")
    # Remove rows where Sales is negative or Quantity is not positive
    df = df[(df["Sales"] >= 0) & (df["Quantity"] > 0)]
    print(f"After filtering: {df.shape}")

    # Calculate additional metrics
    df["processing_time"] = (df["ship_date"] - df["order_date"]).dt.days
    
    # Avoid division by zero for profit margin:
    # Option 1: Set profit margin to 0 when Sales equals 0.
    df["profit_margin_percent"] = np.where(
        df["Sales"] == 0, 0, (df["Profit"] / df["Sales"]) * 100
    )
    
    # Alternatively, Option 2 (if you prefer NULL) could be:
    # df["profit_margin_percent"] = np.where(
    #     df["Sales"] == 0, np.nan, (df["Profit"] / df["Sales"]) * 100
    # )

    # Categorize orders based on Sales amount
    def categorize_sales(value):
        if value < 100:
            return "Small Order"
        elif value <= 500:
            return "Medium Order"
        else:
            return "Large Order"

    df["sales_category"] = df["Sales"].apply(categorize_sales)

    # Convert numeric and object columns to native Python types
    for col in df.select_dtypes(include=["number"]).columns:
        df[col] = df[col].apply(lambda x: x.item() if hasattr(x, "item") and callable(x.item) else x)
    object_cols = df.select_dtypes(include=["object"]).columns
    df[object_cols] = df[object_cols].astype(str)

    print(f"Data cleaned and transformed: {len(df)} rows remaining.")
    return df

def save_transformation(df, out_file_path):
    try:
        print("Saving transformed data...")
        df.to_csv(out_file_path, index=False)
        print(f"Transformed data saved at: {out_file_path}")
    except Exception as e:
        print("Error saving transformed data:", e)

if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    df_cleaned = transform(df)
    print(df_cleaned.info())
    save_transformation(df_cleaned, OUT_FILE_PATH)