import sqlite3
import Scorecard_DB_Manager
import pandas
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