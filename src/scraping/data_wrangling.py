import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import CLEANED_DATA_PATH, RAW_DATA_PATH
from sklearn.impute import KNNImputer
import numpy as np

def impute_missing_data(data, imputation_config=None, n_neighbors=5):
    """
    Handles missing data in a DataFrame using specified imputation techniques.

    Args:
        data (pd.DataFrame): The input DataFrame with potential missing values.
        imputation_config (dict): A dictionary specifying the imputation method for each column.
                                  Example: {'Close': 'mean', 'Adj Close': 'knn'}
                                  If None, applies 'mean' for all columns with missing values.
        n_neighbors (int): Number of neighbors for KNN imputation (only used if method='knn').

    Returns:
        pd.DataFrame: The DataFrame with missing values imputed.
    """
    if imputation_config is None:
        imputation_config = {col: 'mean' for col in data.columns if data[col].isna().sum() > 0}

    for column, method in imputation_config.items():
        if column not in data.columns:
            print(f"Warning: Column '{column}' not found in data. Skipping imputation.")
            continue

        if data[column].isna().sum() == 0:
            print(f"Column '{column}' has no missing values. Skipping imputation.")
            continue

        print(f"Imputing column '{column}' using method: {method}")

        if method == 'mean':
            # Replace missing values with the mean of the column
            mean_value = data[column].mean()
            data[column].fillna(mean_value, inplace=True)

        elif method == 'median':
            # Replace missing values with the median of the column
            median_value = data[column].median()
            data[column].fillna(median_value, inplace=True)

        elif method == 'mode':
            # Replace missing values with the mode of the column
            mode_value = data[column].mode()[0]
            data[column].fillna(mode_value, inplace=True)

        elif method == 'knn':
            # Perform KNN imputation
            imputer = KNNImputer(n_neighbors=n_neighbors)
            data[[column]] = imputer.fit_transform(data[[column]])

        else:
            print(f"Error: Invalid imputation method '{method}' for column '{column}'. Skipping.")

    return data

def wrangle_data(data):
    # Data Wrangling Steps:
    required_columns = ['Close', 'Volume']  # Removed 'Adj Close'
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Warning: Missing columns {missing_columns}. Wrangling may fail.")
        imputation_config = {
            'Close': 'knn',       # Use KNN for the 'Close' column
            'Volume': 'median'    # Use median for the 'Volume' column
        }
        data = impute_missing_data(data, imputation_config)

    # Convert data types (e.g., Ensure 'Date' column is datetime)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(['Symbol', 'Date'])

    # Convert numeric columns to float if needed
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data[numeric_cols] = data[numeric_cols].astype(float)

    # Remove rows where 'Close' is negative
    if 'Close' in data.columns:
        data = data[data['Close'] >= 0]
    
    # Ensure stock symbols are uppercase
    if 'Symbol' in data.columns:
        data['Symbol'] = data['Symbol'].str.upper()

    # Group by 'Ticker' to ensure calculations are done per stock
    grouped = data.groupby('Symbol')

    # Calculate daily percentage change in Close price (percentage change)
    if 'Close' in data.columns:
        data['Close_pct_change'] = grouped['Close'].pct_change()
    # Calculate the percentage change in volume
    data['Volume_pct_change'] = grouped['Volume'].pct_change()

    # Drop any duplicate rows (if any)
    data = data.drop_duplicates()

    # Reset index for cleaner output (optional)
    data.reset_index(drop=True, inplace=True)

    return data

def fetch_clean_data_from_raw(raw_file_name):
    # Construct the full file path
    raw_file_path = os.path.join(RAW_DATA_PATH, raw_file_name)
    print(f"Attempting to load file from: {raw_file_path}")

    # Check if the file exists
    if not os.path.exists(raw_file_path):
        print(f"File {raw_file_path} does not exist.")
        return

    print(f"Loading raw data from: {raw_file_path}")
    df = pd.read_csv(raw_file_path)
    print(f"Columns available in raw data: {df.columns.tolist()}")

    cleaned_data = wrangle_data(df)

     # Ensure the output directory exists
    os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(CLEANED_DATA_PATH, "cleaned_collected_data.csv")

    # Save the cleaned data to a CSV file
    cleaned_data.to_csv(output_file_path, index=False)

    print(f"Data cleaning and wrangling is saved as CSV completed at {output_file_path}")


# List of stock symbols to fetch
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'NVDA', 'META', 'UNH', 'MA', 'LLY',
    'COST', 'V', 'JNJ', 'PG', 'WMT', 'DIS', 'HD', 'BAC', 'XOM', 'CVX',
    'PFE', 'ABBV', 'KO', 'PEP', 'CSCO', 'INTC', 'MRK', 'T', 'VZ', 'ADBE',
    'CRM', 'NFLX', 'PYPL', 'ORCL', 'IBM', 'QCOM', 'AMD', 'TXN', 'NKE', 'MCD',
    'SBUX', 'GS', 'MS', 'C', 'BA', 'CAT', 'GE', 'HON', 'LMT', 'MMM',
    'UPS', 'FDX', 'AMT', 'PLD', 'SPG', 'NOW', 'ZM', 'DOCU', 'SNOW', 'SQ',
    'ROKU', 'SPOT', 'UBER', 'LYFT', 'ABNB', 'SHOP', 'TWLO', 'DDOG', 'OKTA', 'CRWD',
    'ZS', 'NET', 'MDB', 'FSLY', 'PLTR', 'ASML', 'BABA', 'LULU', 'TGT', 'LOW',
    'TJX', 'DG', 'DLTR', 'ROST', 'SNAP', 'TIXT', 'CNQ', 'MNSO', 'D']


# Call the function to fetch data for the given stocks
raw_file_name = "updated_collected_data.csv"
fetch_clean_data_from_raw(raw_file_name)

