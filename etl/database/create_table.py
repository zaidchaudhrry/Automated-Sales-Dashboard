import os
import psycopg2
from dotenv import load_dotenv
from db import connect_to_db  # Adjust this import if needed

# Load environment variables
load_dotenv()

def create_table():
    conn = connect_to_db()
    if conn is None:
        print("Connection to database failed. Exiting.")
        return

    drop_table_query = "DROP TABLE IF EXISTS sales_data CASCADE;"

    create_table_query = """
    CREATE TABLE sales_data (
        category text,
        city text,
        country text,
        customer_id varchar(50),
        customer_name text,
        discount numeric(5,2),
        market text,
        record_count integer,
        order_date date,
        order_id varchar(50) PRIMARY KEY,
        order_priority text,
        product_id varchar(50),
        product_name text,
        profit numeric(10,2),
        quantity integer,
        region text,
        row_id integer,
        sales numeric(10,2),
        segment text,
        ship_date date,
        ship_mode text,
        shipping_cost numeric(10,2),
        state text,
        sub_category text,
        year integer,
        market2 text,
        weeknum integer,
        order_year integer,
        order_month integer,
        week integer,
        day_of_week text,
        processing_time integer,
        profit_margin numeric(10,2),
        sales_category text
    );
    """

    try:
        cur = conn.cursor()

        # Drop the existing table if it exists
        cur.execute(drop_table_query)
        print("Dropped existing 'sales_data' table (if it existed).")

        # Create the new table with the proper schema
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Table 'sales_data' created successfully with the proper transformed schema!")
    except Exception as e:
        print("Error creating table:", e)

if __name__ == "__main__":
    create_table()