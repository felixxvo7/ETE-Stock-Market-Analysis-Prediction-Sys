import os
import pandas as pd
import pandas_ta as ta
from config import PREPROCESSED_DATA_PATH,CLEANED_DATA_PATH

clean_file_name = "cleaned_collected_data.csv"

def read_csv_to_df(clean_file_name):
    """
    Reads a CSV file into a DataFrame.

    Parameters:
        clean_file_name (str): The name of the CSV file to read.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    csv_file_path = os.path.join(CLEANED_DATA_PATH, clean_file_name)
    
    # Ensure the file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: File {csv_file_path} does not exist.")
        return None  # Return None if the file doesn't exist
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    print(f"Loading data from: {csv_file_path}")
    print(f"Columns available in data: {df.columns.tolist()}")

    return df

def add_technical_indicators(data):
    """
    Adds technical indicators to the DataFrame as new columns.

    Parameters:
        data (pd.DataFrame): The DataFrame containing stock data (must include 'Open', 'High', 'Low', 'Close', 'Volume').

    Returns:
        pd.DataFrame: The DataFrame with added technical indicators.
    """
    # Group by 'Symbol' to calculate indicators for each ticker
    grouped = data.groupby('Symbol')

    # Initialize an empty DataFrame to store results
    result_df = pd.DataFrame()

    for ticker, group in grouped:
        # Add technical indicators to each group
        group.ta.sma(length=7, append=True)       # 7-day Simple Moving Average
        group.ta.ema(length=30, append=True)      # 30-day Exponential Moving Average
        group.ta.macd(append=True)                # MACD (12,26,9)
        group.ta.rsi(length=14, append=True)      # 14-day RSI
        group.ta.bbands(length=20, append=True)   # Bollinger Bands (20,2)
        group.ta.atr(length=14, append=True)      # Average True Range (14-day)

        # Append the processed group to the result DataFrame
        result_df = pd.concat([result_df, group], ignore_index=True)

    return result_df

def save_processed_data(data, save_dir=PREPROCESSED_DATA_PATH, output_file_name="processed_data.csv"):
    """
    Saves the processed DataFrame to a CSV file.

    Parameters:
        data (pd.DataFrame): The DataFrame to save.
        save_dir (str): The directory where the processed CSV file will be saved.
        output_file_name (str): The name of the output CSV file.
    """
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    technical_columns = ['Close_pct_change', 'Volume_pct_change','SMA_7', 'EMA_30', 'MACD_12_26_9', 
                         'RSI_14', 'BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'ATRr_14','MACDh_12_26_9','MACDs_12_26_9']
    data = data.dropna(subset=technical_columns)

    # Define the output file path
    output_path = os.path.join(save_dir, output_file_name)

    # Save the DataFrame to CSV
    data.to_csv(output_path, index=False)
    print(f"Processed data saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    # Load the cleaned data
    df = read_csv_to_df(clean_file_name)
    
    if df is not None:
        # Add technical indicators to the DataFrame
        df_with_indicators = add_technical_indicators(df)
        
        # Save the processed DataFrame to a single file
        save_processed_data(df_with_indicators)