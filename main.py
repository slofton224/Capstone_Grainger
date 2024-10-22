import sqlite3
from cost_variance_score import calculate_cost_variance_score
from customer_review import calculate_customer_review_score
from Defect_Rate import calculate_vendor_defect_rate

from post_warranty_score import calculate_post_warranty_score
from pre_warranty_score import calculate_pre_warranty_score
# cost variance score against each item
#score_df = calculate_cost_variance_score()
#print(score_df)

#score_df=calculate_customer_review_score()
#print(score_df)

# defect rate score against each item
#defect_score_df = calculate_vendor_defect_rate()
#print(defect_score_df)


postw_score_df = calculate_post_warranty_score() 
print(postw_score_df)

prew_score_df = calculate_pre_warranty_score()  
print(prew_score_df)