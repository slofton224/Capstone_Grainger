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

# Calculation of the post-warranty vendor return rate
def calculate_post_warranty_return_rate(sales_orders: pd.DataFrame, sales_order_items: pd.DataFrame, 
                                          purchase_orders: pd.DataFrame, purchase_order_items: pd.DataFrame,
                                          materials: pd.DataFrame) -> pd.DataFrame:
    # Merge sales order items with sales orders
    merged_data = sales_order_items.merge(sales_orders, on='so_id', how='left')

    # Merge with purchase_order_items to get po_id
    merged_data = merged_data.merge(purchase_order_items[['po_id', 'mat_id']], on='mat_id', how='left')

    # Merge with purchase orders to get vendor information
    merged_data = merged_data.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')
    
    # Merge with materials to check warranty status
    merged_data = merged_data.merge(materials[['mat_id', 'mat_warranty']], on='mat_id', how='left')

    # Filter for returned items and post-warranty items
    vendor_return_data = merged_data[
        (merged_data['so_returned_against'].notnull()) & 
        (merged_data['mat_warranty'] < merged_data['so_warranty_calculation'])
    ]

    # Group by vendor_id and calculate the total and returned quantities
    return_rate = vendor_return_data.groupby('vendor_id').agg(
        total_quantity=('so_qty', 'sum'),
        returned_quantity=('so_qty', 'count')
    ).reset_index()

    # Calculate the return rate as a percentage
    return_rate['vendor_return_rate'] = (return_rate['returned_quantity'] / return_rate['total_quantity']) * 100

    return return_rate[['vendor_id', 'vendor_return_rate']]

# Main code to fetch data from the database and calculate the return rate
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)

    # List all tables
    tables = list_tables(db_name)
    print("Tables in the database:", tables)

    # Define SQL queries with correct table names
    sales_order_query = """
        SELECT so_id
        FROM sales_order_header;  
    """
    
    sales_order_item_query = """
        SELECT soi.so_id, soi.mat_id, soi.so_qty, soi.so_returned_against, soi.so_warranty_calculation
        FROM sales_order_item soi;  
    """

    purchase_order_query = """
        SELECT po_id, vendor_id 
        FROM purchase_order_header;  
    """
    
    purchase_order_item_query = """
        SELECT po_id, mat_id
        FROM purchase_order_item;
    """
    
    materials_query = """
        SELECT mat_id, mat_warranty
        FROM material_master;
    """

    # Fetch the data into DataFrames
    sales_orders = fetch_data(conn, sales_order_query)
    sales_order_items = fetch_data(conn, sales_order_item_query)
    purchase_orders = fetch_data(conn, purchase_order_query)
    purchase_order_items = fetch_data(conn, purchase_order_item_query)
    materials = fetch_data(conn, materials_query)

    # Close the database connection
    conn.close()

    # Calculate the post-warranty vendor return rate
    return_rate_df = calculate_post_warranty_return_rate(sales_orders, sales_order_items, purchase_orders, purchase_order_items, materials)

    print("Final Post-Warranty Vendor Return Rate DataFrame:")
    print(return_rate_df)

# Run the main function
if __name__ == "__main__":
    main()
