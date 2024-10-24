import sqlite3
import Scorecard_DB_Manager
import pandas as pd
from cost_variance_score import calculate_cost_variance_score
from customer_review_score import calculate_customer_review_score
from defect_rate_score import calculate_vendor_defect_rate
from over_delivered_score import calculate_over_delivery_rate
from under_delivered_score import calculate_under_delivery_rate
from on_time_delivery_score import calculate_on_time_delivery_rate
from post_warranty_score import calculate_post_warranty_score
from pre_warranty_score import calculate_pre_warranty_score
 
# cost variance score against each item
score_cost_variance_df = calculate_cost_variance_score()
print(score_cost_variance_df)

# over delivery rate score against each item 
score_over_delivery_df = calculate_over_delivery_rate()
print(score_over_delivery_df)
 
# Under delivery rate score against each item
score_under_delivered_df = calculate_under_delivery_rate()
print(score_under_delivered_df)

# on time delivery score against each item
score_on_time_df = calculate_on_time_delivery_rate()
print(score_on_time_df)

# customer review score against each item
score_customer_review_df = calculate_customer_review_score()
print(score_customer_review_df)
 
# defect rate score against each item
score_defect_df = calculate_vendor_defect_rate()
print(score_defect_df)
 
# post warranty score against each item
score_postw_df = calculate_post_warranty_score()
print(score_postw_df)

# pre warranty score against each item
score_prew_df = calculate_pre_warranty_score()  
print(score_prew_df)

score_df = score_cost_variance_df[['mat_id', 'cost_variance_score']].merge(score_over_delivery_df[['mat_id', 'over_delivered_score']], on='mat_id', how='left')
score_df = score_df.merge(score_under_delivered_df[['mat_id', 'under_delivered_score']], on='mat_id', how='left')
score_df = score_df.merge(score_on_time_df[['mat_id', 'on_time_delivery_score']], on='mat_id', how='left')
score_df = score_df.merge(score_customer_review_df[['mat_id', 'customer_review_score']], on='mat_id', how='left')
score_df = score_df.merge(score_defect_df[['mat_id', 'defect_rate_score']], on='mat_id', how='left')
score_df = score_df.merge(score_postw_df[['mat_id', 'post_warranty_score']], on='mat_id', how='left')
score_df = score_df.merge(score_prew_df[['mat_id', 'pre_warranty_score']], on='mat_id', how='left')
print(score_df)

# Function to calculate vendor score
def calculate_vendor_score() -> pd.DataFrame:

    dbManager = Scorecard_DB_Manager.ScoreCardDBManager()

    # SQL queries to pull the needed column
    purchase_info_query = """
        SELECT mat_id, vendor_id 
        FROM purchase_info_record;
    """
    vendor_query = """
        SELECT vendor_id, vendor_name
        FROM vendor_master;
    """

    # Store the query outputs in df
    purchase_info = dbManager.fetch_data(purchase_info_query)
    vendor = dbManager.fetch_data(vendor_query)

    # Merging the two DataFrames on 'mat_id' to populate the unit price against each po id
    merged_data = purchase_info.merge(score_df, on='mat_id', how='left')
    print(merged_data)

    # Grouping the merged data by vendor_id into a dataframe to find average scores for all materials belonging to the same vendor
    vendor_score = merged_data.groupby('vendor_id').agg(
        avg_cost_variance_score = ('cost_variance_score', 'mean'), 
        avg_over_delivered_score = ('over_delivered_score', 'mean'),
        avg_under_delivered_score = ('under_delivered_score', 'mean'),
        avg_on_time_delivery_score = ('on_time_delivery_score', 'mean'),
        avg_customer_review_score = ('customer_review_score', 'mean'),
        avg_defect_rate_score = ('defect_rate_score', 'mean'),
        avg_post_warranty_score = ('post_warranty_score', 'mean'),
        avg_pre_warranty_score = ('pre_warranty_score', 'mean'),
    ).reset_index()

    # Calculate vendor score with weights
    vendor_score['vendor_score'] = (
        vendor_score['avg_cost_variance_score'] * 0.15 +
        vendor_score['avg_over_delivered_score'] * 0.05 +
        vendor_score['avg_under_delivered_score'] * 0.12 +
        vendor_score['avg_on_time_delivery_score'] * 0.18 +
        vendor_score['avg_customer_review_score'] * 0.10 +
        vendor_score['avg_defect_rate_score'] * 0.25 +
        vendor_score['avg_post_warranty_score'] * 0.05 +
        vendor_score['avg_pre_warranty_score'] * 0.10
    )

    # Merge with vendor master to pull vendor names
    vendor_score = vendor.merge(vendor_score, on='vendor_id', how='left')

    return vendor_score[['vendor_id', 'vendor_name', 'vendor_score']]

vendor_score_df = calculate_vendor_score()
print(vendor_score_df)