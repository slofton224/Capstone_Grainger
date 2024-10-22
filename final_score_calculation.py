import pandas as pd
from Defect_Rate import calculate_vendor_defect_rate  # Import your function from the defect_rate.py file
from NO_Customer_Reviews import calculate_average_customer_rating # Import function for customer reviews
from NO_Prewarranty_Return_Rate import calculate_vendor_return_rate
from Postwarranty_Return_Rate import calculate_post_warranty_return_rate  # Import functions for return rates
from On_Time_Delivery_Rate import calculate_on_time_delivery_rate#from delivery_performance import calculate_delivery_performance  # Import delivery performance functions
from Over_Delivered import calculate_over_delivery_rate
from cost_variance_score import calculate_cost_variance_score  # Import cost variance functions
 
 
# Function to load vendor metrics
def load_vendor_metrics():
    # Assuming each function returns a DataFrame with vendor_id and the respective metric
    defect_rate_df = calculate_vendor_defect_rate()  # This should return a DataFrame with vendor_id and defect rates
    customer_reviews_df = calculate_average_customer_rating()  # This should return a DataFrame with vendor_id and ratings
    pre_warranty_return_rate_df = calculate_vendor_return_rate()  # Return DataFrame for pre-warranty return rates
    post_warranty_return_rate_df = calculate_post_warranty_return_rate()  # Return DataFrame for post-warranty return rates
    on_time_delivery_rate_df = calculate_on_time_delivery_rate
    over_delivered_df = calculate_over_delivery_rate
    cost_variance_df = calculate_cost_variance_score
   
    #delivery_performance_df = calculate_delivery_performance()  # Return DataFrame for delivery performance metrics
    cost_variance_df = calculate_cost_variance_score()  # Return DataFrame for cost variance
 
    # Merge all metrics into a single DataFrame
    vendor_metrics = defect_rate_df.merge(customer_reviews_df, on='vendor_id', how='outer') \
                                     .merge(pre_warranty_return_rate_df, on='vendor_id', how='outer') \
                                     .merge(post_warranty_return_rate_df, on='vendor_id', how='outer') \
                                     .merge(cost_variance_df, on='vendor_id', how='outer')\
                                     .merge(defect_rate_df,on='vendor_id', how='outer' )\
                                     .merge(on_time_delivery_rate_df, on='vendor_id', how='outer')\
                                     .merge(over_delivered_df,on='vendor_id', how='outer')\
 
    return vendor_metrics
 
# Function to calculate vendor scores
def calculate_vendor_scores(vendor_data):
    scores = []
    for index, row in vendor_data.iterrows():
        # Implement scoring logic based on metrics and weights
        defect_score = max(0, 10 * (1 - row['defect_rate'] / 0.05))  # Adjust this based on your scaling
        # Add additional metrics calculations here
        total_score = defect_score  # Accumulate all scores
        scores.append(total_score)
 
    vendor_data['total_score'] = scores
    return vendor_data[['vendor_id', 'total_score']]
 
# Main code
def main():
    vendor_metrics = load_vendor_metrics()
    vendor_scores = calculate_vendor_scores(vendor_metrics)
    print("Final Vendor Scores DataFrame:")
    print(vendor_scores)
 
if __name__ == "__main__":
    main()
 
 
