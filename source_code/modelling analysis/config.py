# src/config.py

# Headers for HTTP requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

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

VISUALIZED_ACF= 'visualizations/ACF-PACF'