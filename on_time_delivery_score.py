import pandas as pd
import Scorecard_DB_Manager

# Calculation of the on-time delivery rate by vendor
def calculate_on_time_delivery_rate() -> pd.DataFrame:

    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()

    # SQL queries to pull the needed columns
    inbound_delivery_query = """
        SELECT po_id, mat_id, inbound_delivered_date
        FROM inbound_delivery;
    """
    
    purchase_order_query = """
        SELECT po_id, vendor_id, po_delivery_date
        FROM purchase_order_header;
    """
    
    # Storing the query outputs in dataframes
    inbound_delivery = dbManager.fetch_data(inbound_delivery_query)
    purchase_orders = dbManager.fetch_data(purchase_order_query)

    # Merge inbound deliveries with purchase orders to get vendor information and delivery dates
    merged_data = inbound_delivery.merge(purchase_orders[['po_id', 'vendor_id', 'po_delivery_date']], on='po_id', how='left')

    # Convert date columns to datetime for comparison
    merged_data['po_delivery_date'] = pd.to_datetime(merged_data['po_delivery_date'])
    merged_data['inbound_delivered_date'] = pd.to_datetime(merged_data['inbound_delivered_date'])

    # Calculate whether each delivery is on time (True/False)
    merged_data['on_time'] = merged_data['inbound_delivered_date'] <= merged_data['po_delivery_date']

    # Group by vendor_id and calculate the on-time delivery rate
    on_time_rate = merged_data.groupby('mat_id').agg(
        total_deliveries=('po_id', 'count'),
        on_time_deliveries=('on_time', 'sum')
    ).reset_index()

    # Calculate the on-time delivery rate as a percentage
    on_time_rate['on_time_delivery_rate'] = (on_time_rate['on_time_deliveries'] / on_time_rate['total_deliveries']) * 100

    # Scores assigned based on the on_time rate
    def score_on_time(on_time_rate):
        if on_time_rate <= 10:
            return 0
        elif on_time_rate <= 20:
            return 2
        elif on_time_rate <= 30:
            return 4
        elif on_time_rate <= 40:
            return 6
        elif on_time_rate <= 50:
            return 8
        else:
            return 10

    # Applying the scoring function
    on_time_rate['on_time_delivery_score'] = on_time_rate['on_time_delivery_rate'].apply(score_on_time)

    return on_time_rate[['mat_id', 'on_time_delivery_rate', 'on_time_delivery_score']]