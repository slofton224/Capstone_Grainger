import pandas as pd 
import Scorecard_DB_Manager 

# Calculation of the under-delivery rate by vendor
def calculate_under_delivery_rate() -> pd.DataFrame: 

    dbManager = Scorecard_DB_Manager.ScoreCardDBManager() 

    # SQL queries to pull needed columns 
    inbound_delivery_query = """ 
        SELECT po_id, mat_id, inbound_received_qty 
        FROM inbound_delivery;
    """ 

    purchase_order_item_query = """ 
        SELECT po_id, mat_id, po_qty 
        FROM purchase_order_item; 
    """

    #fetching data from the database 
    inbound_delivery = dbManager.fetch_data(inbound_delivery_query) 
    purchase_order_item = dbManager.fetch_data(purchase_order_item_query)

    #merging inbound_delivery with purchase_order_item on 'po_id' and 'mat_id' 
    merged_data = inbound_delivery.merge(purchase_order_item, on=['po_id', 'mat_id'], how='left')

    #calculate quantity under-delivered
    merged_data['under_delivered_qty'] = merged_data['inbound_received_qty'] - merged_data['po_qty']

    #only keep positive values, replace negative values with 0
    merged_data['under_delivered_qty'] = merged_data['under_delivered_qty'].apply(lambda x: abs(x) if x < 0 else 0)
    
    # Group by mat_id and calculate total received and total under-delivered
    under_delivered_rate = merged_data.groupby('mat_id').agg(
        total_received_qty=('inbound_received_qty', 'sum'),
        total_under_delivered_qty=('under_delivered_qty', 'sum')
    ).reset_index()

    # Calculate under-delivered rate as a percentage
    under_delivered_rate['under_delivered_rate'] = (under_delivered_rate['total_under_delivered_qty'] / under_delivered_rate['total_received_qty']) * 100

    #scoring function for under-delivered rates
    def score_under_delivered(under_delivered_rate): 
        if under_delivered_rate == 0: 
            return 10 
        elif under_delivered_rate <= 5: 
            return 8
        elif under_delivered_rate <= 10: 
            return 6 
        elif under_delivered_rate <= 15: 
            return 4 
        elif under_delivered_rate <= 20: 
            return 2 
        else:
            return 0 

    #applying the scoring function 
    under_delivered_rate['under_delivered_score'] = under_delivered_rate['under_delivered_rate'].apply(score_under_delivered) 

    return under_delivered_rate[['mat_id', 'under_delivered_rate', 'under_delivered_score']]