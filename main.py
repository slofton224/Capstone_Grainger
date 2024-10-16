import sqlite3
from cost_variance_score import calculate_cost_variance_score

# cost variance score against each item
score_df = calculate_cost_variance_score()
print(score_df)