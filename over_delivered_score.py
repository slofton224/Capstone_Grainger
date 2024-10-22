import pandas as pd 

import Scorecard_DB_Manager 

 

def calculate_over_delivery_rate() -> pd.DataFrame: 

 

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

     

    purchase_order_query = """ 

        SELECT po_id, vendor_id 

        FROM purchase_order_header; 

    """ 

     

    vendor_master_query = """ 

        SELECT vendor_id, vendor_name 

        FROM vendor_master; 

    """ 

     

    #fetching data from the database 

    inbound_delivery = dbManager.fetch_data(inbound_delivery_query) 

    purchase_order_item = dbManager.fetch_data(purchase_order_item_query) 

    purchase_order_header = dbManager.fetch_data(purchase_order_query) 

    vendor_master = dbManager.fetch_data(vendor_master_query) 

 

    #merging inbound_delivery with purchase_order_item on 'po_id' and 'mat_id' 

    merged_data = inbound_delivery.merge(purchase_order_item, on=['po_id', 'mat_id'], how='left') 

 

    #calculate over-delivery rate 

    merged_data['over_delivery_rate'] = ((merged_data['inbound_received_qty'] - merged_data['po_qty']) / merged_data['po_qty']) * 100 

    merged_data['over_delivery_rate'] = merged_data['over_delivery_rate'].apply(lambda x: x if x > 0 else 0)  # Only positive values, else 0 

 

    #merge with purchase_order_header to get vendor information 

    merged_data = merged_data.merge(purchase_order_header, on='po_id', how='left') 

 

    #scoring function for over-delivered rates 

    def score_over_delivered(over_delivered_rate): 

        if over_delivered_rate == 0: 

            return 10 

        elif over_delivered_rate <= 5: 

            return 8 

        elif over_delivered_rate <= 10: 

            return 6 

        elif over_delivered_rate <= 15: 

            return 4 

        elif over_delivered_rate <= 20: 

            return 2 

        else: 

            return 0 

 

    #applying the scoring function 

    merged_data['over_delivery_score'] = merged_data['over_delivery_rate'].apply(score_over_delivered) 

 

    #merge with vendor_master to get vendor names 

    final_data = merged_data.merge(vendor_master, on='vendor_id', how='left') 

 

    return final_data[[ 'mat_id', 'over_delivery_rate', 'over_delivery_score']]