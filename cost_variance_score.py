import pandas as pd
import Scorecard_DB_Manager

# Connecting to our db
# def connect_to_database(db_name):
#     conn = sqlite3.connect(db_name)
#     return conn

# Fetching data from grainger db
# def fetch_data(conn, query):
#     return pd.read_sql_query(query, conn)

# function defined that will return a dataframe output
def calculate_cost_variance_score() -> pd.DataFrame:

    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()

    # SQL queries to pull the needed columns
    purchase_order_query = """
        SELECT po_id, mat_id, po_unit_cost 
        FROM purchase_order_item;
    """
    material_master_query = """
        SELECT mat_id, mat_unit_cost 
        FROM material_master;
    """

    purchase_info_query = """
        SELECT mat_id, vendor_id 
        FROM purchase_info_record;
    """
    # storing the query outputs in dfs
    purchase_order_item = dbManager.fetch_data(purchase_order_query)
    material_master = dbManager.fetch_data(material_master_query)
    purchase_info = dbManager.fetch_data(purchase_info_query)


    # Merging the two DataFrames on 'mat_id' to populate the unit price against each po id
    merged_data = purchase_order_item.merge(material_master, on='mat_id', how='left')

    # Grouping the merged data by mat_id into a dataframe to find min and max costs across different purchase orders
    cost_variance = merged_data.groupby('mat_id').agg(old_cost=('po_unit_cost', 'min'), new_cost=('po_unit_cost', 'max')).reset_index()

    # Calculating the cost variance
    cost_variance['cost_variance'] = (cost_variance['new_cost'] - cost_variance['old_cost']) / cost_variance['old_cost'] * 100

    # Scores assigned based on the cost variance
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

    # Applying the scoring function
    cost_variance['score'] = cost_variance['cost_variance'].apply(score_variance)
    
    #returning df with score against each item 
    return cost_variance[['mat_id', 'cost_variance', 'score']]

    #merged_vendor = cost_variance.merge(purchase_info, on='mat_id', how='left')

    #return merged_vendor[['vendor_id', 'mat_id', 'cost_variance', 'score']]