import pandas as pd
import Scorecard_DB_Manager

# Calculation of average customer ratings by vendor
def calculate_customer_review_score() -> pd.DataFrame:
    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()
    
    customer_review_query = """
        SELECT so_id, customer_rating
        FROM customer_review;
    """
    sales_item_query = """
        SELECT so_id, mat_id
        FROM sales_order_item;
    """
    purchase_info_query = """
        SELECT vendor_id, mat_id
        FROM purchase_info_record;
    """
    # Fetch the data into DataFrames
    customer_reviews = dbManager.fetch_data(customer_review_query)
    purchase_info = dbManager.fetch_data(purchase_info_query)
    sales_order_items = dbManager.fetch_data(sales_item_query)  # Corrected here
    
    merged_data = customer_reviews.merge(sales_order_items, on='so_id', how='left')
     
    average_rating = merged_data.groupby('mat_id').agg(average_customer_rating=('customer_rating', 'mean')).reset_index()
   
    def score_rating(rating):  # Used integers (out of 10) instead of percentage
        if rating < 4:
            return 0
        elif rating <= 5:
            return 2
        elif rating <= 6:
            return 4
        elif rating <= 7:
            return 6
        elif rating <= 8:
            return 8
        else:
            return 10
 
    average_rating['score'] = average_rating['average_customer_rating'].apply(score_rating)

    return average_rating[['mat_id', 'average_customer_rating', 'score']]  # Include the score in the return
