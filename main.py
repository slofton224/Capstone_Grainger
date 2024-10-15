import sqlite3
import Scorecard_DB_Manager

#preparing for PowerBI script
pip install pandas
pip install matplotlib

dbManager = Scorecard_DB_Manager.ScoreCardDBManager()
data = dbManager.ReadAllData()

#Print Database rows
for val in data.fetchall():
    print(val)

#test comment
#testing pushing and pulling
