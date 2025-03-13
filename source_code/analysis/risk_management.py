import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import DATABASE_PATH

# **User-defined risk parameters**
RISK_PER_TRADE = 0.02  # 2% risk per trade
STOP_LOSS_MULTIPLIER = 2  # Stop-loss = 2x ATR
MAX_SECTOR_EXPOSURE = 0.25  # 25% max exposure per sector

def retrieve_stock_data(table="full_stock_data"):
    """Retrieve stock data from SQLite database"""
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    conn = sqlite3.connect(db_file_path)
    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# **Load stock data**
df = retrieve_stock_data()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# **Manually Assign Sectors to Stocks**
sector_mapping = {
    'AAPL': 'Tech', 'MSFT': 'Tech', 'GOOGL': 'Tech', 'META': 'Tech', 'NVDA': 'Tech',
    'AMZN': 'E-commerce', 'TSLA': 'Auto', 'BABA': 'E-commerce',
    'JPM': 'Finance', 'BAC': 'Finance', 'GS': 'Finance', 'MS': 'Finance',
    'XOM': 'Energy', 'CVX': 'Energy', 'OXY': 'Energy', 'COP': 'Energy',
    'PG': 'Consumer Goods', 'KO': 'Consumer Goods', 'PEP': 'Consumer Goods', 'WMT': 'Consumer Goods',
    'NKE': 'Consumer Goods', 'MCD': 'Consumer Goods', 'HD': 'Retail',
    'UNH': 'Healthcare', 'PFE': 'Healthcare', 'JNJ': 'Healthcare', 'MRK': 'Healthcare', 'LLY': 'Healthcare',
    'GE': 'Industrials', 'LMT': 'Industrials', 'CAT': 'Industrials',
    'DIS': 'Entertainment', 'NFLX': 'Entertainment', 'SPOT': 'Entertainment'
}

# **Filter out stocks without assigned sectors**
df['Sector'] = df['Symbol'].map(sector_mapping)
df = df.dropna(subset=['Sector'])  # Remove rows where sector is NaN

# **Calculate ATR (Average True Range) for Stop-Loss Setting**
df['ATR'] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(14).std())  # Approximate ATR

# **Risk Per Trade Calculation**
portfolio_size = 100000  # Example: $100,000 total portfolio value
risk_per_trade = portfolio_size * RISK_PER_TRADE  # Risk per trade (e.g., $2,000 for 2% risk)

# **Calculate Position Size Based on ATR**
df['Position_Size'] = risk_per_trade / (STOP_LOSS_MULTIPLIER * df['ATR'])  # Shares to buy per stock

# **Check Sector Exposure**
sector_weights = df.groupby('Sector')['Position_Size'].sum() / df['Position_Size'].sum()
overexposed_sectors = sector_weights[sector_weights > MAX_SECTOR_EXPOSURE]

# **Adjust Exposure If Needed**
if not overexposed_sectors.empty:
    print("\nWARNING: Overexposed Sectors Found! Adjusting Allocation:")
    print(overexposed_sectors)
    for sector in overexposed_sectors.index:
        df.loc[df['Sector'] == sector, 'Position_Size'] *= MAX_SECTOR_EXPOSURE / overexposed_sectors[sector]

# **Rebalancing: Reduce Exposure to Overweight Stocks**
df['Weight'] = df['Position_Size'] / df['Position_Size'].sum()  # Normalize weights
df = df[df['Weight'] > 0]  # Remove stocks with zero allocation

# **Save Final Risk-Managed Portfolio**
risk_managed_file = "risk_managed_portfolio.csv"
df[['Symbol', 'Position_Size', 'Weight', 'Sector']].to_csv(risk_managed_file, index=False)
print(f"\nRisk-managed portfolio saved to {risk_managed_file}")

# **Print Final Risk-Managed Portfolio**
print("\nFinal Risk-Managed Portfolio:\n")
print(df[['Symbol', 'Position_Size', 'Weight', 'Sector']])

# **Save and Print Sector Allocation**
sector_weights_df = df.groupby('Sector')['Weight'].sum().reset_index()
sector_weights_file = "sector_allocation.csv"
sector_weights_df.to_csv(sector_weights_file, index=False)
print(f"\nSector Allocation saved to {sector_weights_file}")
print("\nSector Allocation:\n")
print(sector_weights_df)

# **Plot Sector Allocation**
sector_weights_df.set_index('Sector')['Weight'].plot(kind='bar', title="Sector Diversification", figsize=(8, 5))
plt.xlabel("Sector")
plt.ylabel("Portfolio Weight")
plt.show()
