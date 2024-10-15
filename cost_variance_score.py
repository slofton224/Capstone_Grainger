import pandas as pd
import sqlite3

# Connecting to our db
def connect_to_database(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Fetching data from grainger db
def fetch_data(conn, query):
    return pd.read_sql_query(query, conn)

# Calculation of the cost variance score by creating two dataframes
def calculate_cost_variance_score(purchase_order_item: pd.DataFrame, material_master: pd.DataFrame) -> pd.DataFrame:
    # Merging the two DataFrames on 'mat_id' to bring in the unit prices
    merged_data = purchase_order_item.merge(material_master, on='mat_id', how='left')

    # Group by 'mat_id' to find min and max costs across different purchase orders
    cost_variance = merged_data.groupby('mat_id').agg(old_cost=('po_unit_cost', 'min'), new_cost=('po_unit_cost', 'max')).reset_index()

    # Calculate the cost variance
    cost_variance['cost_variance'] = (cost_variance['new_cost'] - cost_variance['old_cost']) / cost_variance['old_cost'] * 100

    # Assign scores based on the cost variance
    def score_variance(variance):
        if variance <= 10:
            return 10
        elif variance <= 20:
            return 8
        elif variance <= 30:
            return 6
        elif variance <= 40:
            return 4
        elif variance <= 50:
            return 2
        else:
            return 0

    # Apply the scoring function
    cost_variance['score'] = cost_variance['cost_variance'].apply(score_variance)

    return cost_variance[['mat_id', 'cost_variance', 'score']]

# Main code to fetch data from the database and calculate the score
def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)

    # Define your SQL queries
    purchase_order_query = """
        SELECT po_id, mat_id, po_unit_cost 
        FROM purchase_order_item;
    """
    material_master_query = """
        SELECT mat_id, mat_unit_cost 
        FROM material_master;
    """

    # Fetch the data into DataFrames
    purchase_order_item = fetch_data(conn, purchase_order_query)
    material_master = fetch_data(conn, material_master_query)

    # Close the database connection
    conn.close()

    # Calculate the cost variance score
    score_df = calculate_cost_variance_score(purchase_order_item, material_master)

    print(score_df)

# Run the main function
if __name__ == "__main__":
    main()
