import sqlite3
import pandas as pd
import os
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

from config import DATABASE_PATH, PREPROCESSED_DATA_PATH

# Define the folder to save ACF and PACF plots
VISUALIZED_ACF = "visualizations/ACF-PACF"
os.makedirs(VISUALIZED_ACF, exist_ok=True)  # Create the folder if it doesn't exist

def retrieve_data(table="full_stock_data"):
    """
    Retrieve data from the specified table in the SQLite database.

    Parameters:
        table (str): The name of the table to retrieve data from.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved data.
                     Returns None if an error occurs.
    """
    # Step 1: Connect to the Database
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    try:
        conn = sqlite3.connect(db_file_path)
        print(f"Connected to database at: {db_file_path}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        print("Check if the database file exists and the path is correct.")
        return None

    # Step 2: Execute a SQL Query
    query = f"SELECT * FROM {table}"
    try:
        data_df = pd.read_sql(query, conn)
        print("Data retrieved successfully:")
        print(data_df.head())  # Display the first few rows
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        # Step 3: Close the Database Connection
        conn.close()
        print("Database connection closed.")

    return data_df

def test_stationarity(timeseries):
    """
    Perform the Augmented Dickey-Fuller test to check for stationarity.

    Parameters:
        timeseries (pd.Series): The time series data to test.

    Returns:
        dict: A dictionary containing the test results.
    """
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = {
        "Test Statistic": dftest[0],
        "p-value": dftest[1],
        "#Lags Used": dftest[2],
        "Number of Observations Used": dftest[3],
        "Critical Value (1%)": dftest[4]["1%"],
        "Critical Value (5%)": dftest[4]["5%"],
        "Critical Value (10%)": dftest[4]["10%"],
    }
    return dfoutput

def make_stationary(timeseries):
    """
    Make the time series stationary by applying differencing.

    Parameters:
        timeseries (pd.Series): The time series data to transform.

    Returns:
        pd.Series: The stationary time series.
    """
    stationary_series = timeseries.diff().dropna()  # First-order differencing
    return stationary_series

def plot_acf_pacf(timeseries, symbol, lags=40):
    """
    Plot the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF).

    Parameters:
        timeseries (pd.Series): The time series data to analyze.
        symbol (str): The stock symbol (used for saving the plot).
        lags (int): The number of lags to include in the plots.

    Returns:
        None (saves the ACF and PACF plots to the VISUALIZED_ACF folder).
    """
    # Plot ACF and PACF
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plot_acf(timeseries, lags=lags, ax=plt.gca())
    plt.title(f"Autocorrelation Function (ACF) for {symbol}")

    plt.subplot(2, 1, 2)
    plot_pacf(timeseries, lags=lags, ax=plt.gca())
    plt.title(f"Partial Autocorrelation Function (PACF) for {symbol}")

    plt.tight_layout()

    # Save the plot
    plot_filename = os.path.join(VISUALIZED_ACF, f"{symbol}_ACF_PACF.png")
    plt.savefig(plot_filename)
    plt.close()
    print(f"Saved ACF and PACF plot for {symbol} at {plot_filename}")

def save_stationary_data_to_db(stationary_data, db_path=DATABASE_PATH):
    """
    Save the stationary-transformed data for all symbols to a single table in the SQLite database.

    Parameters:
        stationary_data (pd.DataFrame): The combined stationary-transformed data for all symbols.
        db_path (str): The path to the SQLite database.
    """
    db_file_path = os.path.join(db_path, "stocks_database.db")
    conn = sqlite3.connect(db_file_path)

    # Create a new table for the stationary data
    table_name = "stationary_data_all"
    stationary_data.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Saved all stationary data in table '{table_name}'.")

    # Close the connection
    conn.close()

def process_all_symbols(data_df):
    """
    Process all unique stock symbols in the dataset:
    - Test for stationarity.
    - Transform non-stationary data.
    - Generate ACF and PACF plots.
    - Save all stationary data to a single table in the database.

    Parameters:
        data_df (pd.DataFrame): The DataFrame containing the stock data.
    """
    # Get all unique symbols
    unique_symbols = data_df["Symbol"].unique()
    print(f"Found {len(unique_symbols)} unique symbols: {unique_symbols}")

    # Initialize a list to store stationarity test results and stationary data
    stationarity_results = []
    all_stationary_data = []

    for symbol in unique_symbols:
        print(f"\nProcessing symbol: {symbol}")

        # Filter data for the current symbol
        symbol_data = data_df[data_df["Symbol"] == symbol]

        # Use the 'Close' column for time series analysis
        timeseries = symbol_data["Close"]

        # Step 1: Test for stationarity
        print(f"Testing stationarity for {symbol}...")
        stationarity_result = test_stationarity(timeseries)
        stationarity_result["Symbol"] = symbol  # Add symbol to the result
        stationarity_results.append(stationarity_result)

        # Step 2: If the data is non-stationary, make it stationary
        if stationarity_result["p-value"] > 0.05:
            print(f"Data for {symbol} is non-stationary. Applying differencing...")
            stationary_series = make_stationary(timeseries)
            print(f"Stationary data for {symbol} created.")
        else:
            print(f"Data for {symbol} is already stationary.")
            stationary_series = timeseries

        # Step 3: Generate ACF and PACF plots
        print(f"Generating ACF and PACF plots for {symbol}...")
        plot_acf_pacf(stationary_series, symbol)

        # Step 4: Prepare stationary data for saving
        stationary_data = symbol_data.copy()
        stationary_data["Close"] = stationary_series  # Replace with stationary data
        all_stationary_data.append(stationary_data)

    # Combine all stationary data into a single DataFrame
    combined_stationary_data = pd.concat(all_stationary_data, ignore_index=True)

    # Step 5: Save all stationary data to the database
    save_stationary_data_to_db(combined_stationary_data)

    # Save stationarity test results to a CSV file
    results_df = pd.DataFrame(stationarity_results)
    results_df.to_csv(os.path.join(VISUALIZED_ACF, "stationarity_test_results.csv"), index=False)
    print("\nStationarity test results saved to 'stationarity_test_results.csv'.")

# Example usage
if __name__ == "__main__":
    # Retrieve data from the database
    stock_data_df = retrieve_data(table="full_stock_data")

    if stock_data_df is not None:
        # Process all unique symbols
        process_all_symbols(stock_data_df)