import sqlite3
import pandas as pd
import os
from config import CLEANED_DATA_PATH  # Ensure CLEANED_DATA_PATH is defined in your config

# Function to connect to the SQLite database and load data into a pandas DataFrame
def load_data_from_db(db_name='stocks_data.db', table_names=['scraped_stock_data', 'collected_stock_data']):
    db_file_path = os.path.join(CLEANED_DATA_PATH, db_name)  # Adjust the path if necessary
    conn = sqlite3.connect(db_file_path)

    # Load data into pandas DataFrame for both tables
    dfs = {}
    for table_name in table_names:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, conn)
        dfs[table_name] = df
    
    # Close the connection
    conn.close()

    return dfs

# Function to export data to Excel for Power BI
def export_to_excel(dfs, filename="stocks_data_for_powerbi.xlsx"):
    # Save each DataFrame to a separate sheet in the Excel file
    with pd.ExcelWriter(os.path.join(CLEANED_DATA_PATH, filename), engine='openpyxl') as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Data exported to {filename}")

# Main function
def main():
    # Load the data from the database (from two tables)
    dfs = load_data_from_db()

    # Export data to Excel
    export_to_excel(dfs)

if __name__ == "__main__":
    main()
