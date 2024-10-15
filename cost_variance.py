    #creating 
def calculate_cost_variance_score(purchase_order_items: pd.DataFrame, material_master: pd.DataFrame) -> pd.DataFrame:
    # Merging the two DataFrames on 'mat_id' to bring in the unit prices
    merged_data = purchase_order_items.merge(material_master, on='mat_id', how='left', suffixes=('', '_original'))

    # Calculate the cost variance
    merged_data['cost_variance'] = (merged_data['new_cost'] - merged_data['old_cost']) / merged_data['old_cost'] * 100

    # Assign scores based on the cost variance
    def score_variance(variance):
        if variance <= 10:
            return 10
        elif variance <= 20:
            return 8
        elif variance <= 30:
            return 6
        elif variance <= 40:
            return 4
        elif variance <= 50:
            return 2
        else:
            return 0

    # Apply the scoring function
    merged_data['score'] = merged_data['cost_variance'].apply(score_variance)

    return merged_data[['mat_id', 'cost_variance', 'score']]

# Example DataFrames for demonstration purposes
purchase_order_items = pd.DataFrame({
    'mat_id': [1, 2, 1, 3],
    'old_cost': [100, 200, 100, 300],
    'new_cost': [105, 220, 130, 310]
})

material_master = pd.DataFrame({
    'mat_id': [1, 2, 3],
    'unit_price': [100, 200, 300]
})

# Calculate the cost variance score
score_df = calculate_cost_variance_score(purchase_order_items, material_master)

print(score_df)
