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

# Calculation of the on-time delivery rate by vendor
def calculate_on_time_delivery_rate(inbound_delivery: pd.DataFrame, purchase_orders: pd.DataFrame, vendors: pd.DataFrame) -> pd.DataFrame:
    # Merge inbound deliveries with purchase orders to get vendor information and delivery dates
    merged_data = inbound_delivery.merge(purchase_orders[['po_id', 'vendor_id', 'po_delivery_date']], on='po_id', how='left')

    # Convert date columns to datetime for comparison
    merged_data['po_delivery_date'] = pd.to_datetime(merged_data['po_delivery_date'])
    merged_data['inbound_delivered_date'] = pd.to_datetime(merged_data['inbound_delivered_date'])

    # Calculate whether each delivery is on time (True/False)
    merged_data['on_time'] = merged_data['inbound_delivered_date'] <= merged_data['po_delivery_date']

    # Group by vendor_id and calculate the on-time delivery rate
    on_time_data = merged_data.groupby('vendor_id').agg(
        total_deliveries=('po_id', 'count'),
        on_time_deliveries=('on_time', 'sum')
    ).reset_index()

    # Calculate the on-time delivery rate as a percentage
    on_time_data['on_time_delivery_rate'] = (on_time_data['on_time_deliveries'] / on_time_data['total_deliveries']) * 100

    # Merge with vendor names for readability
    on_time_data = on_time_data.merge(vendors[['vendor_id', 'vendor_name']], on='vendor_id', how='left')

    return on_time_data[['vendor_id', 'vendor_name', 'on_time_delivery_rate']]

# Main code to fetch data from the database and calculate the on-time delivery rate
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)

    # List all tables
    tables = list_tables(db_name)
    print("Tables in the database:", tables)

    # Define SQL queries for relevant tables
    inbound_delivery_query = """
        SELECT po_id, inbound_delivered_date
        FROM inbound_delivery;
    """
    
    purchase_order_query = """
        SELECT po_id, vendor_id, po_delivery_date
        FROM purchase_order_header;
    """
    
    vendor_master_query = """
        SELECT vendor_id, vendor_name
        FROM vendor_master;
    """

    # Fetch the data into DataFrames
    inbound_delivery = fetch_data(conn, inbound_delivery_query)
    purchase_orders = fetch_data(conn, purchase_order_query)
    vendors = fetch_data(conn, vendor_master_query)

    # Close the database connection
    conn.close()

    # Calculate the vendor on-time delivery rate
    on_time_delivery_rate_df = calculate_on_time_delivery_rate(inbound_delivery, purchase_orders, vendors)

    print("Final Vendor On-Time Delivery Rate DataFrame:")
    print(on_time_delivery_rate_df)

# Run the main function
if __name__ == "__main__":
    main()
