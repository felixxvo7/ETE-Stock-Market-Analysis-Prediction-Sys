import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import RAW_DATA_PATH

def fetch_stock_data(stocks):
    # Get today's date and calculate the date one year ago
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

    # Initialize an empty list to store the data
    all_data = []

    # Loop through the stock symbols and fetch the data
    for stock in stocks:
        print(f"Fetching data for {stock}...")
        
        try:
            # Download historical stock data
            stock_data = yf.download(stock, start=start_date, end=end_date)
            
            # Check if data was returned (some symbols might fail to fetch)
            if stock_data.empty:
                print(f"No data found for {stock}. Skipping...")
                continue
            
            # Add the stock symbol as a new column
            stock_data['Symbol'] = stock
            
            # Append the data to the list
            all_data.append(stock_data)
        
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            continue

    # Combine the data for all stocks into one DataFrame
    if all_data:
        combined_data = pd.concat(all_data)

        # Ensure the output directory exists
        os.makedirs(RAW_DATA_PATH, exist_ok=True)

        # Define the output file path
        output_file_path = os.path.join(RAW_DATA_PATH, "raw_collected_1year_data.csv")

        # Save the data to a CSV file
        combined_data.to_csv(output_file_path)
        
        print(f"Data collection and saving to CSV completed at {output_file_path}")
    else:
        print("No data was collected for any stock.")

# List of stock symbols to fetch
stocks = ['SNAP', 'ABNB', 'SHOP', 'TIXT', 'CNQ', 'NFLX', 'PG', 'WMT', 'MNSO', 'D']

# Call the function to fetch data for the given stocks
fetch_stock_data(stocks)
