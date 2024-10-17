import pandas as pd
import sqlite3

# Connecting to the database
def connect_to_database(db_name):
    return sqlite3.connect(db_name)

# Fetching data from the database
def fetch_data(conn, query):
    return pd.read_sql_query(query, conn)

# List tables in the database
def list_tables(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return tables

# Calculation of average customer ratings by vendor
def calculate_average_customer_rating(customer_reviews: pd.DataFrame, sales_order_items: pd.DataFrame, purchase_order_items: pd.DataFrame, purchase_orders: pd.DataFrame, vendor_master: pd.DataFrame) -> pd.DataFrame:
    # Merge customer reviews with sales order items to connect so_id with mat_id
    merged_data = customer_reviews.merge(sales_order_items[['so_id', 'mat_id']], on='so_id', how='left')
    # Merge with purchase order items to get po_id and vendor information
    merged_data = merged_data.merge(purchase_order_items[['po_id', 'mat_id']], on='mat_id', how='left')
    # Merge with purchase orders to get vendor information
    merged_data = merged_data.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')
    # Group by vendor_id and calculate the average rating
    average_rating = merged_data.groupby('vendor_id').agg(
        average_customer_rating=('customer_rating', 'mean')
    ).reset_index()
    # Merge with vendor_master to get vendor names
    average_rating = average_rating.merge(vendor_master, on='vendor_id', how='left')
    return average_rating[['vendor_id', 'vendor_name', 'average_customer_rating']]

# Main code to fetch data from the database and calculate the average customer rating
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)
    # List all tables
    tables = list_tables(db_name)
    print("Tables in the database:", tables)
    # Define SQL queries with correct table names
    customer_review_query = """
        SELECT so_id, customer_rating
        FROM customer_review;
    """
    sales_order_item_query = """
        SELECT so_id, mat_id
        FROM sales_order_item;
    """
    purchase_order_item_query = """
        SELECT po_id, mat_id
        FROM purchase_order_item;
    """
    purchase_order_query = """
        SELECT po_id, vendor_id
        FROM purchase_order_header;
    """
    vendor_master_query = """
        SELECT vendor_id, vendor_name
        FROM vendor_master;
    """
    # Fetch the data into DataFrames
    customer_reviews = fetch_data(conn, customer_review_query)
    sales_order_items = fetch_data(conn, sales_order_item_query)
    purchase_order_items = fetch_data(conn, purchase_order_item_query)
    purchase_orders = fetch_data(conn, purchase_order_query)
    vendor_master = fetch_data(conn, vendor_master_query)
    # Close the database connection
    conn.close()
    # Calculate the average customer rating by vendor
    average_rating_df = calculate_average_customer_rating(customer_reviews, sales_order_items, purchase_order_items, purchase_orders, vendor_master)
    print("Vendor Average Customer Ratings DataFrame:")
    print(average_rating_df)

# Run the main function
if __name__ == "__main__":
    main()
