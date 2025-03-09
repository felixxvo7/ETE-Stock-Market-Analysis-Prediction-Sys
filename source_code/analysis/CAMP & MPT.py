import sqlite3
import pandas as pd
import os
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.plotting import plot_efficient_frontier
from config import DATABASE_PATH

def retrieve_data(table="full_stock_data"):
    """Retrieve data from SQLite database"""
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    try:
        conn = sqlite3.connect(db_file_path)
        print(f"Connected to database at: {db_file_path}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        print("Check if the database file exists and the path is correct.")
        return None

    query = f"SELECT * FROM {table}"
    try:
        data_df = pd.read_sql(query, conn)
        print("Data retrieved successfully:")
        print(data_df.head())  # Display the first few rows
        print(f"Columns: {data_df.columns.tolist()}")  # Print column names
        print(f"Unique Symbols: {data_df['Symbol'].unique()}")  # Print unique symbols
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()
        print("Database connection closed.")

    return data_df

def fetch_market_data(market_ticker="^GSPC", start_date=None, end_date=None):
    """
    Fetch market index data using yfinance
    
    Parameters:
        market_ticker (str): Ticker symbol for the market index (default: S&P 500)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
        pd.Series: Market index returns
    """
    # Fetch market data
    market_data = yf.download(market_ticker, start=start_date, end=end_date)['Adj Close']
    market_returns = market_data.pct_change().dropna()
    return market_returns

def calculate_capm_returns(data_df, risk_free_rate=0.02, market_ticker="^GSPC"):
    """
    Calculate CAPM expected returns using yfinance for market data
    """
    # Fetch market data
    start_date = data_df['Date'].min()
    end_date = data_df['Date'].max()
    market_returns = fetch_market_data(market_ticker, start_date=start_date, end_date=end_date)
    
    # Prepare stock returns
    close_prices = data_df.pivot(index='Date', columns='Symbol', values='Close')
    stock_returns = close_prices.pct_change().dropna()
    
    # Align market and stock returns
    common_dates = stock_returns.index.intersection(market_returns.index)
    if len(common_dates) == 0:
        raise ValueError("No common dates between market and stock returns.")
    
    stock_returns = stock_returns.loc[common_dates]
    market_returns = market_returns.loc[common_dates]
    
    # Calculate CAPM parameters
    covariance = stock_returns.apply(lambda x: np.cov(x, market_returns)[0, 1])
    beta = covariance / market_returns.var()
    market_premium = market_returns.mean() - risk_free_rate/252  # Daily premium
    
    # CAPM formula (annualized)
    expected_returns = risk_free_rate + beta * market_premium * 252
    return expected_returns

def optimize_portfolio(data_df, target_return=0.15):
    """
    Optimize portfolio using Modern Portfolio Theory
    """
    # Prepare data
    close_prices = data_df.pivot(index='Date', columns='Symbol', values='Close')
    
    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(close_prices)
    S = risk_models.sample_cov(close_prices)
    
    # Optimize portfolio
    ef = EfficientFrontier(mu, S)
    ef.add_constraint(lambda w: w >= 0)  # No shorting
    ef.add_constraint(lambda w: w.sum() == 1)  # Fully invested
    ef.efficient_return(target_return=target_return)
    
    return ef.clean_weights()

def portfolio_analysis():
    """Main portfolio optimization workflow with yfinance for CAPM"""
    # Retrieve data from database
    data_df = retrieve_data()
    if data_df is None:
        return
    
    # Convert date column
    data_df['Date'] = pd.to_datetime(data_df['Date'])
    
    try:
        # CAPM Analysis with yfinance
        print("\nCalculating CAPM Expected Returns...")
        capm_returns = calculate_capm_returns(data_df)
        print("CAPM Expected Returns:")
        print(capm_returns)
        
        # Portfolio Optimization
        print("\nOptimizing Portfolio...")
        optimized_weights = optimize_portfolio(data_df)
        print("Optimized Portfolio Weights:")
        for symbol, weight in optimized_weights.items():
            if weight > 0.01:
                print(f"{symbol}: {weight*100:.2f}%")
        
        # Efficient Frontier Visualization
        print("\nPlotting Efficient Frontier...")
        close_prices = data_df.pivot(index='Date', columns='Symbol', values='Close')
        mu = expected_returns.mean_historical_return(close_prices)
        S = risk_models.sample_cov(close_prices)
        
        plt.figure(figsize=(10, 6))
        plot_efficient_frontier(EfficientFrontier(mu, S), show_assets=True)
        plt.title("Efficient Frontier with Technical Indicators")
        plt.xlabel("Annualized Risk (Volatility)")
        plt.ylabel("Annualized Return")
        plt.show()
        
        # Additional metrics using technical indicators
        print("\nTechnical Indicator Statistics:")
        print(data_df.groupby('Symbol')[['RSI_14', 'ATRr_14', 'BBP_20_2.0']].mean())
        
    except Exception as e:
        print(f"Error in portfolio analysis: {e}")

if __name__ == "__main__":
    portfolio_analysis()