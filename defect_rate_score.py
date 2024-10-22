import pandas as pd
import Scorecard_DB_Manager

# Connecting to the database
# def connect_to_database(db_name):
#    return sqlite3.connect(db_name)

# Fetching data from the database
# def fetch_data(conn, query):
#    return pd.read_sql_query(query, conn)

# List tables in the database
# def list_tables(db_name):
#    conn = sqlite3.connect(db_name)
#    cursor = conn.cursor()
#    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#    tables = cursor.fetchall()
#    conn.close()
#    return tables

# Calculation of the defect rate by vendor
def calculate_vendor_defect_rate() -> pd.DataFrame:

    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()

    # SQL queries to pull the needed columns
    inbound_delivery_query = """
        SELECT po_id, mat_id, inbound_received_qty, inbound_failed_qty
        FROM inbound_delivery;  
    """
    
    purchase_order_query = """
        SELECT po_id, vendor_id
        FROM purchase_order_header;  
    """
    #purchase_info_query = """
    #    SELECT mat_id, vendor_id 
    #    FROM purchase_info_record;
    #"""

    # Storing the query outputs in dataframes
    inbound_delivery = dbManager.fetch_data(inbound_delivery_query)
    purchase_orders = dbManager.fetch_data(purchase_order_query)
    #purchase_info = dbManager.fetch_data(purchase_info_query)

    # Merge inbound deliveries with purchase orders to get vendor information (no mat_id in purchase_orders)
    merged_data = inbound_delivery.merge(purchase_orders[['po_id', 'vendor_id']], on='po_id', how='left')

    # Group by mat_id and calculate total received and failed quantities
    defect_rate = merged_data.groupby('mat_id').agg(
        total_received_qty=('inbound_received_qty', 'sum'),
        total_failed_qty=('inbound_failed_qty', 'sum')
    ).reset_index()

    # Calculate defect rate as a percentage
    defect_rate['defect_rate'] = (defect_rate['total_failed_qty'] / defect_rate['total_received_qty']) * 100

    # Scores assigned based on the defect rate
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
    defect_rate['score'] = defect_rate['defect_rate'].apply(score_defect)

    #merged_vendor = defect_rate.merge(purchase_info, on='mat_id', how='left')

    return defect_rate[['mat_id', 'defect_rate', 'score']]

