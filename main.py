import sqlite3
from cost_variance_score import calculate_cost_variance_score
from Defect_Rate import calculate_vendor_defect_rate

# cost variance score against each item
score_df = calculate_cost_variance_score()
print(score_df)

# defect rate score against each item
defect_score_df = calculate_vendor_defect_rate()
print(defect_score_df)