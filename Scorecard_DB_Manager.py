import sqlite3

class ScoreCardDBManager:

    def __init__(self):
        self.DBName = "Grainger_DB.db"
        self.conn = sqlite3.connect(self.DBName)

#reading tables: material master 
    def ReadAllData(self):
        dbReadSql = "SELECT * FROM Material_Master"
        tableValues = self.conn.execute(dbReadSql)
        return tableValues
    
    #reading tables: material master 
    def ReadData(self, table_name):
        dbReadSql = "SELECT * FROM" + table_name
        tableValues = self.conn.execute(dbReadSql)
        return tableValues
