import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import RAW_DATA_PATH

def fetch_stock_data(stocks):
    # Get today's date and calculate the date one year ago
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=410)).strftime('%Y-%m-%d')  # Strictly 1 year

    # Initialize an empty list to store the data
    all_data = []
    failed_stocks = []  # To keep track of stocks that failed to fetch

    # Loop through the stock symbols and fetch the data
    for stock in stocks:
        print(f"Fetching data for {stock}...")
        
        try:
            # Download historical stock data
            stock_data = yf.download(stock, start=start_date, end=end_date)
            
            # Check if data was returned (some symbols might fail to fetch)
            if stock_data.empty:
                print(f"No data found for {stock}. Skipping...")
                failed_stocks.append((stock, "No data found"))
                continue
            
            # Add the stock symbol and company name as new columns
            try:
                stock_info = yf.Ticker(stock).info
                company_name = stock_info.get('longName', 'N/A')  # Use 'longName' for the full company name
            except Exception as e:
                print(f"Error fetching company info for {stock}: {e}")
                company_name = 'N/A'
            
            stock_data['Symbol'] = stock
            stock_data['Company'] = company_name
            
            # Reset the index to ensure 'Date' becomes a column
            stock_data.reset_index(inplace=True)
            
            # Append the data to the list
            all_data.append(stock_data)
        
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            failed_stocks.append((stock, str(e)))
            continue

    # Combine the data for all stocks into one DataFrame
    if all_data:
        # Ensure all data frames have the same columns
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Symbol', 'Company']
        all_data = [df[columns] for df in all_data]
        
        combined_data = pd.concat(all_data, ignore_index=True)

        # Ensure the output directory exists
        os.makedirs(RAW_DATA_PATH, exist_ok=True)

        # Define the output file path
        output_file_path = os.path.join(RAW_DATA_PATH, "raw_collected_1year_data.csv")

        # Save the data to a CSV file
        combined_data.to_csv(output_file_path, index=False)
        
        print(f"Data collection and saving to CSV completed at {output_file_path}")
    else:
        print("No data was collected for any stock.")

    # Print failed stocks (if any)
    if failed_stocks:
        print("\nFailed to fetch data for the following stocks:")
        for stock, error in failed_stocks:
            print(f"- {stock}: {error}")

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
fetch_stock_data(stocks)