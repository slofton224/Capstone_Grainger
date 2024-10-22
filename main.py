import sqlite3
from cost_variance_score import calculate_cost_variance_score
from customer_review import calculate_customer_review_score
from Defect_Rate import calculate_vendor_defect_rate
from Over_Delivered import calculate_over_delivery_rate 
from Under_Delivered import calculate_under_delivery_rate 
# cost variance score against each item
#score_df = calculate_cost_variance_score()
#print(score_df)


#over delivery rate for each item 

score_over_delivery_df = calculate_over_delivery_rate() 

print (score_over_delivery_df) 



# Under delivery rate for each item 

# score_under_delivered_df = calculate_under_delivery_rate 

# print(score_under_delivered_df) 

# score_df=calculate_customer_review_score()
# print(score_df)

# # defect rate score against each item
# defect_score_df = calculate_vendor_defect_rate()
# print(defect_score_df)