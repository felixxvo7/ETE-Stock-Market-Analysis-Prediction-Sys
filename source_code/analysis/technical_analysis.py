import os
import pandas as pd
import mplfinance as mpf
import pandas_ta as ta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from config import PREPROCESSED_DATA_PATH, DATABASE_PATH
import sqlite3

processed_file_name = "processed_data.csv"

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


# Function to generate and save candlestick charts
def generate_candlestick_chart(data, symbol, save_dir="visualizations"):
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlesticks'
    )])
    
    # Add technical indicators
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA_7'],
        mode='lines',
        name='7-day SMA',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['EMA_30'],
        mode='lines',
        name='30-day EMA',
        line=dict(color='orange')
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['BBL_20_2.0'],
        mode='lines',
        name='Bollinger Lower Band',
        line=dict(color='green', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['BBU_20_2.0'],
        mode='lines',
        name='Bollinger Upper Band',
        line=dict(color='red', dash='dash')
    ))
    
    # Customize layout
    fig.update_layout(
        title=f"{symbol} Candlestick Chart with Indicators",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    
    # Save as HTML and PNG
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    fig.write_html(f"{save_dir}/{symbol}_candlestick.html")

def detect_doji(row):
    """
    Detect Doji pattern: A candle with a very small body.
    """
    body_size = abs(row['Close'] - row['Open'])
    candle_range = row['High'] - row['Low']
    # Doji condition: small body relative to the candle range
    return body_size <= 0.01 * candle_range  # Adjust threshold as needed

def detect_engulfing(data):
    """
    Detect Engulfing pattern: A candle that completely engulfs the previous candle.
    """
    engulfing = []
    for i in range(1, len(data)):
        prev_open, prev_close = data.iloc[i-1]['Open'], data.iloc[i-1]['Close']
        curr_open, curr_close = data.iloc[i]['Open'], data.iloc[i]['Close']
        # Bullish engulfing: current candle engulfs the previous candle
        if curr_close > curr_open and prev_close < prev_open and curr_open < prev_close and curr_close > prev_open:
            engulfing.append(1)
        # Bearish engulfing: current candle engulfs the previous candle
        elif curr_close < curr_open and prev_close > prev_open and curr_open > prev_close and curr_close < prev_open:
            engulfing.append(-1)
        else:
            engulfing.append(0)
    # Add a 0 for the first row (no previous candle to compare)
    engulfing.insert(0, 0)
    return engulfing

def detect_hammer(row):
    """
    Detect Hammer pattern: A candle with a small body and a long lower wick.
    """
    body_size = abs(row['Close'] - row['Open'])
    candle_range = row['High'] - row['Low']
    lower_wick = min(row['Close'], row['Open']) - row['Low']
    # Hammer condition: small body, long lower wick
    return body_size <= 0.1 * candle_range and lower_wick >= 0.6 * candle_range

def detect_patterns(data, symbol, db_path= DATABASE_PATH):
    # Create a copy of the data to avoid SettingWithCopyWarning
    data = data.copy()
    
    # Detect patterns using custom logic
    data.loc[:, 'CDLDOJI'] = data.apply(detect_doji, axis=1)
    data.loc[:, 'CDLENGULFING'] = detect_engulfing(data)
    data.loc[:, 'CDLHAMMER'] = data.apply(detect_hammer, axis=1)
    
    # Filter rows where patterns are detected
    patterns = data[(data['CDLDOJI'] == 1) | (data['CDLENGULFING'] != 0) | (data['CDLHAMMER'] == 1)]
    
    # Add symbol column
    patterns.loc[:, 'Symbol'] = symbol
    
    # Store results in SQLite database
    db_file_path = os.path.join(db_path, "detected_patterns")
    conn = sqlite3.connect(db_file_path)
    patterns.to_sql("detected_patterns", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    # Load the cleaned data
    clean_file_name = read_csv_to_df(processed_file_name)

    # Group data by 'Symbols' column
    grouped_data = clean_file_name.groupby('Symbol')

# Generate charts for each stock
    for symbol, group in grouped_data:
        generate_candlestick_chart(group, symbol) 
        detect_patterns(group, symbol)