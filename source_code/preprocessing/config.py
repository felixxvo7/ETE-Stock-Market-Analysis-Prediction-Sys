# src/config.py

# Headers for HTTP requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

#Stocks

STOCKS = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'NVDA', 'META', 'UNH', 'MA', 'LLY',
            'COST', 'V', 'JNJ', 'PG', 'WMT', 'DIS', 'HD', 'BAC', 'XOM', 'CVX',
            'PFE', 'ABBV', 'KO', 'PEP', 'CSCO', 'INTC', 'MRK', 'T', 'VZ', 'ADBE',
            'CRM', 'NFLX', 'PYPL', 'ORCL', 'IBM', 'QCOM', 'AMD', 'TXN', 'NKE', 'MCD',
            'SBUX', 'GS', 'MS', 'C', 'BA', 'CAT', 'GE', 'HON', 'LMT', 'MMM',
            'UPS', 'FDX', 'AMT', 'PLD', 'SPG', 'NOW', 'ZM', 'DOCU', 'SNOW', 'SQ',
            'ROKU', 'SPOT', 'UBER', 'LYFT', 'ABNB', 'SHOP', 'TWLO', 'DDOG', 'OKTA', 'CRWD',
            'ZS', 'NET', 'MDB', 'FSLY', 'PLTR', 'ASML', 'BABA', 'LULU', 'TGT', 'LOW',
            'TJX', 'DG', 'DLTR', 'ROST', 'SNAP', 'TIXT', 'CNQ', 'MNSO', 'D']
    

# URLs to scrape
URLS = [
    'https://www.cnbc.com/quotes/SNAP?qsearchterm=snap',
    'https://www.cnbc.com/quotes/ABNB?qsearchterm=air',
    'https://www.cnbc.com/quotes/SHOP?qsearchterm=shopify',
    'https://www.cnbc.com/quotes/TIXT?qsearchterm=tixt',
    'https://www.cnbc.com/quotes/AMZN?qsearchterm=amazonQ',
    'https://www.cnbc.com/quotes/CNQ?qsearchterm=cnq',
    'https://www.cnbc.com/quotes/NFLX?qsearchterm=nflx',
    'https://www.cnbc.com/quotes/PG?qsearchterm=pg',
    'https://www.cnbc.com/quotes/WMT?qsearchterm=wmt',
    'https://www.cnbc.com/quotes/MNSO?qsearchterm=mini',
    'https://www.cnbc.com/quotes/D?qsearchterm=d'
]

# Output folder for raw data
RAW_DATA_PATH = 'data/raw_data'

CLEANED_DATA_PATH = 'data/cleaned_data'

PREPROCESSED_DATA_PATH = 'data/processed_data/merged'

DATABASE_PATH = 'data/database'