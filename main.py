import sqlite3
import Scorecard_DB_Manager

dbManager = Scorecard_DB_Manager.ScoreCardDBManager()
data = dbManager.ReadAllData()

#Print Database rows
for val in data.fetchall():
    print(val)
