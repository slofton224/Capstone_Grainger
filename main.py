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
#score_df = calculate_cost_variance_score()
#print(score_df)
 

#over delivery rate for each item 
#score_over_delivery_df = calculate_over_delivery_rate()
#print (score_over_delivery_df)
 
# Under delivery rate for each item
# score_under_delivered_df = calculate_under_delivery_rate
# print(score_under_delivered_df)

#on time delivery
#on_time_df = calculate_on_time_delivery_rate()
#print(on_time_df)

#customer review score 
# score_df=calculate_customer_review_score()
# print(score_df)
 
# defect rate score against each item
# defect_score_df = calculate_vendor_defect_rate()
# print(defect_score_df)
 
#post warranty 
#postw_score_df = calculate_post_warranty_score()
#print(postw_score_df)

#pre warranty 
#prew_score_df = calculate_pre_warranty_score()  
#print(prew_score_df)