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

# Calculation of the under-delivery rate by vendor
def calculate_under_delivery_rate(inbound_delivery: pd.DataFrame, purchase_order_items: pd.DataFrame, purchase_orders: pd.DataFrame, vendors: pd.DataFrame) -> pd.DataFrame:
    # Merge inbound deliveries with purchase order items to get ordered quantities and material info
    merged_data = inbound_delivery.merge(purchase_order_items[['po_id', 'mat_id', 'po_qty']], on=['po_id', 'mat_id'], how='left')

    # Merge with purchase orders to get vendor information
    merged_data = merged_data.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')

    # Calculate whether each delivery is under-delivered (True/False)
    merged_data['under_delivered'] = merged_data['inbound_received_qty'] < merged_data['po_qty']

    # Group by vendor_id and calculate total deliveries and under-delivered deliveries
    under_delivery_data = merged_data.groupby('vendor_id').agg(
        total_deliveries=('po_id', 'count'),
        under_delivered_count=('under_delivered', 'sum')
    ).reset_index()

    # Calculate the under-delivery rate as a percentage
    under_delivery_data['under_delivery_rate'] = (under_delivery_data['under_delivered_count'] / under_delivery_data['total_deliveries']) * 100

    # Merge with vendor names for readability
    under_delivery_data = under_delivery_data.merge(vendors[['vendor_id', 'vendor_name']], on='vendor_id', how='left')

    return under_delivery_data[['vendor_id', 'vendor_name', 'under_delivery_rate']]

# Main code to fetch data from the database and calculate the under-delivery rate
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)

    # List all tables
    tables = list_tables(db_name)
    print("Tables in the database:", tables)

    # Define SQL queries for relevant tables
    inbound_delivery_query = """
        SELECT po_id, mat_id, inbound_received_qty
        FROM inbound_delivery;
    """
    
    purchase_order_item_query = """
        SELECT po_id, mat_id, po_qty
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
    inbound_delivery = fetch_data(conn, inbound_delivery_query)
    purchase_order_items = fetch_data(conn, purchase_order_item_query)
    purchase_orders = fetch_data(conn, purchase_order_query)
    vendors = fetch_data(conn, vendor_master_query)

    # Close the database connection
    conn.close()

    # Calculate the vendor under-delivery rate
    under_delivery_rate_df = calculate_under_delivery_rate(inbound_delivery, purchase_order_items, purchase_orders, vendors)

    print("Final Vendor Under-Delivery Rate DataFrame:")
    print(under_delivery_rate_df)

# Run the main function
if __name__ == "__main__":
    main()
