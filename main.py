import sqlite3
import Scorecard_DB_Manager

#define the vendor class and vendor scorecard
class Vendor:
	def__init__(self,quality_metrics, delivery_metrics, cost_metrics):
        self.quality_metrics = quality_metrics
        self.delivery_metrics = delivery_metrics
        self.cost_metrics = cost_metrics
    def calculate_score(self):
        quality_score = self.calculate_weighted_score(self.quality_metrics)
        delivery_score = self.calculate_weighted_score(self.delivery_metrics)
        cost_score = self.calculate_weighted_score(self.cost_metrics) 
		
		#defining the weights for the metrics
		w1 = 0.25  # Weight for Defect Rate
        w2 = 0.10  # Weight for Customer Rating
        w3 = 0.10  # Weight for Customer Return Rate (Pre-W)
        w4 = 0.05  # Weight for Customer Return Rate (Post-W)
        w5 = 0.18  # Weight for On-Time Delivery
        w6 = 0.05  # Weight for Quantity Over Delivered
        w7 = 0.12  # Weight for Quantity Under Delivered
        w8 = 0.15  # Weight for Cost Variance

        #calculate vendor score with the weights 
        detailed_scores = {
            'Defect Rate': w1 * quality_score[0],
            'Customer Rating': w2 * quality_score[1],
            'Customer Return Rate (Pre-W)': w3 * quality_score[2],
            'Customer Return Rate (Post-W)': w4 * quality_score[3],
            'On-Time Delivery': w5 * delivery_score[0],
            'Quantity Over Delivered': w6 * delivery_score[1],
            'Quantity Under Delivered': w7 * delivery_score[2],
            'Cost Variance': w8 * cost_score[0]
        }

        #sum of detailed score
        vendor_score = sum(detailed_scores.values())
        return vendor_score, detailed_scores







dbManager = Scorecard_DB_Manager.ScoreCardDBManager()
data = dbManager.ReadAllData()

#Print Database rows
for val in data.fetchall():
    print(val)

#test comment

#Does this work
