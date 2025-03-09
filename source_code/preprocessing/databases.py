import os
import pandas as pd
import sqlite3
from config import PREPROCESSED_DATA_PATH, DATABASE_PATH

def read_csv_to_df(clean_file_name):
    """
    Reads a CSV file into a DataFrame.

    Parameters:
        clean_file_name (str): The name of the CSV file to read.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    csv_file_path = os.path.join(PREPROCESSED_DATA_PATH, clean_file_name)
    
    # Ensure the file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: File {csv_file_path} does not exist.")
        return None  # Return None if the file doesn't exist
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    print(f"Loading data from: {csv_file_path}")
    print(f"Columns available in data: {df.columns.tolist()}")

    return df

def import_full_stock_data(clean_file_name, db_path=DATABASE_PATH):
    """
    Imports the full stock data into the SQLite database.

    Parameters:
        clean_file_name (str): The name of the CSV file containing the processed stock data.
        db_path (str): The path to the SQLite database.
    """
    # Load the cleaned data
    df = read_csv_to_df(clean_file_name)
    if df is None:
        return  # Exit if the file doesn't exist
    
    # Store results in SQLite database
    db_file_path = os.path.join(db_path, "stocks_database.db")
    conn = sqlite3.connect(db_file_path)
    
    # Write the full stock data to the 'full_stock_data' table
    df.to_sql("full_stock_data", conn, if_exists="replace", index=False)
    print("Full stock data imported successfully into 'full_stock_data' table.")
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    # Import full stock data
    processed_file_name = "processed_data.csv"
    import_full_stock_data(processed_file_name)