import pandas as pd
import Scorecard_DB_Manager

def calculate_pre_warranty_score() -> pd.DataFrame:
    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()

    # SQL query to fetch data from sales_order_item table
    sales_order_item_query = """
        SELECT so_id, mat_id, so_qty, so_returned_against, so_pre_post_warranty 
        FROM sales_order_item;
    """

    # Fetching the sales order items data
    sales_order_item = dbManager.fetch_data(sales_order_item_query)

    # Filtering for pre-warranty items
    pre_warranty_items = sales_order_item[sales_order_item['so_pre_post_warranty'] == 'Pre-warranty']

    # Calculating total quantities sold and returned quantities
    total_sold = sales_order_item.groupby('mat_id')['so_qty'].sum().reset_index(name='total_qty_sold')
    returned_qty = pre_warranty_items.groupby('mat_id')['so_qty'].sum().reset_index(name='returned_qty')

    # Merging total sold and returned quantities
    summary = total_sold.merge(returned_qty, on='mat_id', how='left').fillna(0)

    # Calculating pre warranty ratio
    summary['pre_warranty_ratio'] = summary['returned_qty'] / summary['total_qty_sold']
    
    # Function to assign scores based on post warranty ratio
    def score_pre_warranty(ratio):
        if ratio <= 0.05:  # 0-5%
            return 10
        elif ratio <= 0.10:  # 6-10%
            return 8
        elif ratio <= 0.15:  # 11-15%
            return 6
        elif ratio <= 0.20:  # 16-20%
            return 4
        elif ratio <= 0.25:  # 21-25%
            return 2
        else:  # >25%
            return 0

    # Applying the scoring function
    summary['pre_warranty_score'] = summary['pre_warranty_ratio'].apply(score_pre_warranty)

    # Returning the DataFrame with mat_id, post warranty ratio, and score
    return summary[['mat_id', 'pre_warranty_ratio', 'pre_warranty_score']]

# Example of calling the function
# df_post_warranty_score = calculate_post_warranty_score()
