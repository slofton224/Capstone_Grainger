# import pandas as pd
# import sqlite3

# # Connecting to the database
# def connect_to_database(db_name):
#     return sqlite3.connect(db_name)

# # Fetching data from the database
# def fetch_data(conn, query):
#     return pd.read_sql_query(query, conn)

# # List tables in the database
# def list_tables(db_name):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()
#     conn.close()
#     return tables

# # Fetch column names for a specific table
# def fetch_columns(conn, table_name):
#     cursor = conn.cursor()
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     columns = cursor.fetchall()
#     return columns

# # Main function to list tables and their columns
# def main():
#     # Connect to the database
#     db_name = 'Grainger_DB.db'
#     conn = connect_to_database(db_name)

#     # List all tables
#     tables = list_tables(db_name)
#     print("Tables in the database:")
#     for table in tables:
#         table_name = table[0]
#         print(f"\nTable: {table_name}")
        
#         # Fetch and print column names for each table
#         columns = fetch_columns(conn, table_name)
#         print("Columns:")
#         for col in columns:
#             print(f" - {col[1]} (Type: {col[2]})")  # col[1] is the column name, col[2] is the data type
    
#     # Close the database connection
#     conn.close()

# # Run the main function
# if __name__ == "__main__":
#     main()



def check_data_presence(conn):
    queries = [
        "SELECT COUNT(*) FROM inbound_delivery;",
        "SELECT COUNT(*) FROM purchase_info_record;",
        "SELECT COUNT(*) FROM customer_review;",
        "SELECT COUNT(*) FROM purchase_order_header;",
        "SELECT COUNT(*) FROM purchase_order_item;"
    ]
    
    for query in queries:
        count_df = fetch_data(conn, query)
        print(f"Count for query '{query}': {count_df.iloc[0, 0]}")

def main():
    # Connect to the database
    db_name = 'Grainger_DB.db'
    conn = connect_to_database(db_name)
    
    # Check data presence
    check_data_presence(conn)

