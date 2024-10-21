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

# Calculation of the defect rate by vendor
def calculate_vendor_defect_rate(inbound_delivery: pd.DataFrame, purchase_orders: pd.DataFrame, vendors: pd.DataFrame) -> pd.DataFrame:
    # Merge inbound deliveries with purchase orders to get vendor information
    merged_data = inbound_delivery.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')

    # Group by vendor_id and calculate total received and failed quantities
    defect_data = merged_data.groupby('vendor_id').agg(
        total_received_qty=('inbound_received_qty', 'sum'),
        total_failed_qty=('inbound_failed_qty', 'sum')
    ).reset_index()

    # Calculate defect rate as a percentage
    defect_data['defect_rate'] = (defect_data['total_failed_qty'] / defect_data['total_received_qty']) * 100

    # Merge with vendor names to make it more readable
    defect_data = defect_data.merge(vendors[['vendor_id', 'vendor_name']], on='vendor_id', how='left')

    return defect_data[['vendor_id', 'vendor_name', 'defect_rate']]

# Main code to fetch data from the database and calculate the defect rate
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)

    # List all tables
    tables = list_tables(db_name)
    print("Tables in the database:", tables)

    # Define SQL queries for relevant tables
    inbound_delivery_query = """
        SELECT po_id, inbound_received_qty, inbound_failed_qty
        FROM inbound_delivery;  
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
    purchase_orders = fetch_data(conn, purchase_order_query)
    vendors = fetch_data(conn, vendor_master_query)

    # Close the database connection
    conn.close()

    # Calculate the vendor defect rate
    defect_rate_df = calculate_vendor_defect_rate(inbound_delivery, purchase_orders, vendors)

    print("Final Vendor Defect Rate DataFrame:")
    print(defect_rate_df)

    def score_defect(defect):
        if defect <= 5:
            return 10
        elif defect <= 10:
            return 8
        elif defect <= 15:
            return 6
        elif defect <= 20:
            return 4
        elif defect <= 25:
            return 2
        else:
            return 0

    # Applying the scoring function
    defect_rate_df['score'] = defect_rate_df['defect_rate'].apply(score_defect)

    # Print the df with score for each item
    print(defect_rate_df[['vendor_id', 'vendor_name', 'defect_rate', 'score']])

    #returning df with score against each item 
    return defect_rate_df[['vendor_id', 'vendor_name', 'defect_rate', 'score']]

# Run the main function
if __name__ == "__main__":
    main()
