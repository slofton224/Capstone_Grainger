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

# Calculation of the vendor return rate
def calculate_vendor_return_rate(sales_orders: pd.DataFrame, sales_order_items: pd.DataFrame, purchase_orders: pd.DataFrame, purchase_order_items: pd.DataFrame) -> pd.DataFrame:
    # Merge sales order items with sales orders
    merged_data = sales_order_items.merge(sales_orders, on='so_id', how='left')

    # Merge with purchase_order_items to get po_id
    merged_data = merged_data.merge(purchase_order_items[['po_id', 'mat_id']], on='mat_id', how='left')

    # Merge with purchase orders to get vendor information
    merged_data = merged_data.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')

    # Filter for returned items (where so_returned_against is not null)
    vendor_return_data = merged_data[merged_data['so_returned_against'].notnull()]

    # Group by vendor_id and calculate the total and returned quantities
    return_rate = vendor_return_data.groupby('vendor_id').agg(
        returned_quantity=('so_qty', 'count')
    ).reset_index()

    # Add total quantity per vendor (from all orders, not just returns)
    total_quantity = merged_data.groupby('vendor_id').agg(
        total_quantity=('so_qty', 'sum')
    ).reset_index()

    # Merge total quantities with return quantities
    vendor_data = total_quantity.merge(return_rate, on='vendor_id', how='left')

    # Fill missing returned quantities with 0 (for vendors with no returns)
    vendor_data['returned_quantity'] = vendor_data['returned_quantity'].fillna(0)

    # Calculate the return rate as a percentage
    vendor_data['vendor_return_rate'] = (vendor_data['returned_quantity'] / vendor_data['total_quantity']) * 100

    return vendor_data[['vendor_id', 'vendor_return_rate']]

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
        SELECT soi.so_id, soi.mat_id, soi.so_qty, soi.so_returned_against
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

    # Fetch the data into DataFrames
    sales_orders = fetch_data(conn, sales_order_query)
    sales_order_items = fetch_data(conn, sales_order_item_query)
    purchase_orders = fetch_data(conn, purchase_order_query)
    purchase_order_items = fetch_data(conn, purchase_order_item_query)

    # Close the database connection
    conn.close()

    # Calculate the vendor return rate
    return_rate_df = calculate_vendor_return_rate(sales_orders, sales_order_items, purchase_orders, purchase_order_items)

    print("Final Vendor Return Rate DataFrame:")
    print(return_rate_df)

    def score_return(return_rate):
        if return_rate <= 5:
            return 10
        elif return_rate <= 10:
            return 8
        elif return_rate <= 15:
            return 6
        elif return_rate <= 20:
            return 4
        elif return_rate <= 25:
            return 2
        else:
            return 0

    # Applying the scoring function
    return_rate_df['score'] = return_rate_df['vendor_return_rate'].apply(score_return)

    # Print the df with score for each item
    print(return_rate_df[['vendor_id', 'vendor_return_rate', 'score']])

    #returning df with score against each item 
    return return_rate_df[['vendor_id', 'vendor_return_rate', 'score']]

# Run the main function
if __name__ == "__main__":
    main()
