import sqlite3
import pandas as pd

class ScoreCardDBManager:

    def __init__(self):
        self.DBName = "Grainger_DB.db"
        self.conn = sqlite3.connect(self.DBName)

#reading tables: material master 
    # def ReadAllData(self):
    #     dbReadSql = "SELECT * FROM sales_order"
    #     tableValues = self.conn.execute(dbReadSql)
    #     return tableValues
    
    # #reading tables: material master 
    # def ReadData(self, table_name):
    #     dbReadSql = "SELECT * FROM " +" "+ table_name
    #     tableValues = self.conn.execute(dbReadSql)
    #     return tableValues
    
    # Fetching data from grainger db by using pd.read_sql_query() and returning a dataframe 
    def fetch_data(self, query):
        return pd.read_sql_query(query, self.conn)
