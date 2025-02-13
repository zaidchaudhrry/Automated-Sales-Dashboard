import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from database.db import connect_to_db  # Adjust this import if needed

# Load environment variables
load_dotenv()

# Define the file path for the transformed CSV data
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANSFORMED_FILE_PATH = os.path.join(BASE_DIR, "data", "transformed_superstore.csv")

def load_transformed_data():
    print("Starting transformed data insertion...")

    conn = connect_to_db()
    if conn is None:
        print("Connection to database failed. Exiting.")
        return

    try:
        print(f"Reading transformed data from: {TRANSFORMED_FILE_PATH}")
        df = pd.read_csv(TRANSFORMED_FILE_PATH)
        print(f"Transformed DataFrame loaded with {len(df)} rows.")

        cur = conn.cursor()

        # Insert query matching the 34 columns of the transformed table schema.
        insert_query = """
            INSERT INTO sales_data (
                category, city, country, customer_id, customer_name, discount, market,
                record_count, order_date, order_id, order_priority, product_id, product_name,
                profit, quantity, region, row_id, sales, segment, ship_date, ship_mode,
                shipping_cost, state, sub_category, year, market2, weeknum, order_year,
                order_month, week, day_of_week, processing_time, profit_margin, sales_category
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """

        inserted = 0
        for _, row in df.iterrows():
            values = (
                row["Category"],             # category
                row["City"],                 # city
                row["Country"],              # country
                row["Customer.ID"],          # customer_id
                row["Customer.Name"],        # customer_name
                row["Discount"],             # discount
                row["Market"],               # market
                row["记录数"],                # record_count
                row["order_date"],           # order_date (transformed/renamed)
                row["Order.ID"],             # order_id
                row["Order.Priority"],       # order_priority
                row["Product.ID"],           # product_id
                row["Product.Name"],         # product_name
                row["Profit"],               # profit
                row["Quantity"],             # quantity
                row["Region"],               # region
                row["Row.ID"],               # row_id
                row["Sales"],                # sales
                row["Segment"],              # segment
                row["ship_date"],            # ship_date (transformed/renamed)
                row["Ship.Mode"],            # ship_mode
                row["Shipping.Cost"],        # shipping_cost
                row["State"],                # state
                row["Sub.Category"],         # sub_category
                row["Year"],                 # year
                row["Market2"],              # market2
                row["weeknum"],              # weeknum
                row["order_year"],           # order_year (new column)
                row["order_month"],          # order_month (new column)
                row["week"],                 # week (new column)
                row["day_of_week"],          # day_of_week (new column)
                row["processing_time"],      # processing_time (new column)
                row["profit_margin_percent"],# profit_margin (mapped from profit_margin_percent)
                row["sales_category"]        # sales_category (new column)
            )
            cur.execute(insert_query, values)
            inserted += 1
            if inserted % 1000 == 0:
                print(f"Inserted {inserted} rows...")

        conn.commit()
        cur.close()
        conn.close()
        print(f"{inserted} transformed records inserted successfully!")
    except Exception as e:
        print("Error inserting transformed data:", e)

if __name__ == "__main__":
    load_transformed_data()