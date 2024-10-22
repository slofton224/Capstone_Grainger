import sqlite3
import pandas as pd

class ScoreCardDBManager:

    def __init__(self):
        self.DBName = "Grainger_DB.db"
        self.conn = sqlite3.connect(self.DBName)

    def __del__(self):
        self.conn.close()

    # Fetching data from the database using pd.read_sql_query()
    def fetch_data(self, query):
        return pd.read_sql_query(query, self.conn)

    # Method to perform SQL transformations
    def perform_sql_transformations(self):
        # SQL for warranty calculation (date difference)
        warranty_calculation_sql = '''
        UPDATE sales_order_item
        SET so_warranty_calculation = (
            SELECT 
                julianday(header_original.so_created_on) - julianday(header_returned.so_created_on)
            FROM 
                sales_order_header AS header_original
            JOIN sales_order_header AS header_returned
                ON sales_order_item.so_returned_against = header_returned.so_id
            WHERE 
                sales_order_item.so_id = header_original.so_id
        )
        WHERE so_returned_against IS NOT NULL;
        '''
        
        # SQL for determining pre- or post-warranty
        pre_post_warranty_sql = '''
        UPDATE sales_order_item
        SET so_pre_post_warranty = (
            CASE 
                WHEN so_warranty_calculation <= (
                    SELECT mat_warranty 
                    FROM material_master 
                    WHERE material_master.mat_id = sales_order_item.mat_id
                ) THEN 'Pre-warranty'
                ELSE 'Post-warranty'
            END
        )
        WHERE so_warranty_calculation IS NOT NULL
        AND EXISTS (
            SELECT 1 
            FROM material_master 
            WHERE material_master.mat_id = sales_order_item.mat_id
        );
        '''
        
        # Execute the warranty calculation SQL
        self.conn.execute(warranty_calculation_sql)
        self.conn.commit()
        
        # Execute the pre- or post-warranty SQL
        self.conn.execute(pre_post_warranty_sql)
        self.conn.commit()

# Example usage of the class
if __name__ == "__main__":
    # Create an instance of the ScoreCardDBManager class
    db_manager = ScoreCardDBManager()

    # Perform SQL transformations
    db_manager.perform_sql_transformations()

    # Fetch data to verify transformations (optional)
    df = db_manager.fetch_data("SELECT * FROM sales_order_item")
    print(df)
