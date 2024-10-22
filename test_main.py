import sqlite3
from On_Time_Delivery_Rate import calculate_on_time_delivery_rate
from Defect_Rate import calculate_vendor_defect_rate

on_time_df = calculate_on_time_delivery_rate()
print(on_time_df)

defect_score_df = calculate_vendor_defect_rate()
print(defect_score_df)