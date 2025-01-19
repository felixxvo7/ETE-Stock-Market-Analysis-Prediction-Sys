import os
import sqlite3
import pandas as pd
from config import CLEANED_DATA_PATH, RAW_DATA_PATH

raw_file_name = "cleaned_collected_data.csv"

def read_clean_data(raw_file_name):
    raw_file_path = os.path.join(CLEANED_DATA_PATH, raw_file_name)
    print(f"Attempting to load file from: {raw_file_path}")

    if not os.path.exists(raw_file_path):
        print(f"File {raw_file_path} does not exist.")
        return None

    print(f"Loading raw data from: {raw_file_path}")
    df = pd.read_csv(raw_file_path)
    print(f"Columns available in raw data: {df.columns.tolist()}")

    # Convert the 'Date' column to datetime (if not already in that format)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

    return df



def store_data_in_db(db_name='stocks_data.db', table_name='collected_stock_data'):
    # Construct the full path to the database file in CLEANED_DATA_PATH
    db_file_path = os.path.join(CLEANED_DATA_PATH, db_name)

    # Step 1: Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 2: Create the table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE ,
        close REAL,
        adj_close REAL,
        volume INTEGER,
        symbol TEXT,
        close_pct_change REAL,
        volume_pct_change REAL,
        "7_day_ma" REAL  -- Wrap the column name starting with a number in double quotes
    );
    """
    cursor.execute(create_table_query)

    # Read the cleaned data
    data = read_clean_data(raw_file_name)
    
    if data is None:
        print("Data not loaded. Exiting database insertion.")
        conn.close()
        return
    
    print(f"Data is storing in SQLite database!")

    # Step 3: Insert data into the table
    try:
        for index, row in data.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (
                date, close, adj_close, volume, symbol,
                close_pct_change, volume_pct_change, "7_day_ma"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (
                row['Date'], row['Close'], row['Adj Close'], row['Volume'], row['Symbol'],
                row['Close_pct_change'], row['Volume_pct_change'], row['7_Day_MA']
            ))
        
        print(f"Data stored in SQLite database successfully!")
    except Exception as e:
        print(f"Error inserting data into database: {e}")

    # Commit and close the connection
    conn.commit()
    conn.close()

def store_scraped_data_in_db(db_name='stocks_data.db', table_name='scraped_stock_data'):
    # Load the scraped CSV data into a DataFrame
    csv_file_path = os.path.join(RAW_DATA_PATH, 'raw_scraped_stocks_data.csv')
    
    # Ensure the file exists
    if not os.path.exists(csv_file_path):
        print(f"File {csv_file_path} does not exist.")
        return
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Step 1: Connect to the SQLite database (it will be created if it doesn't exist)
    db_file_path = os.path.join(CLEANED_DATA_PATH, db_name)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 2: Create the table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        price REAL,
        change TEXT,
        percentage TEXT,
        volume INTEGER
    );
    """
    cursor.execute(create_table_query)

    # Step 3: Insert the scraped data into the database
    try:
        for index, row in df.iterrows():
            insert_query = f"""
            INSERT INTO {table_name} (company, price, change, percentage, volume) 
            VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (
                row['Company'], row['Price'], row['Change'], row['Percentage'], row['Volume']
            ))
        
        print(f"Data stored in SQLite database successfully!")
    except Exception as e:
        print(f"Error inserting data into database: {e}")

    # Commit and close the connection
    conn.commit()
    conn.close()

# Call the function to store the scraped data into the database
store_scraped_data_in_db()
store_data_in_db()
