import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from datetime import datetime
from config import URLS, HEADERS, RAW_DATA_PATH  # Import configurations

# Define regex patterns
pattern = r"^(.*?)-"
price_pattern = r"Close([\d\.]+)"
change_pattern = r"([+-][\d\.]+)"
percentage_pattern = r"\(([+-][\d\.%]+)\)"
volume_pattern = r"Volume([\d,]+)"

def scrape_and_save():
    all_data = []  # Initialize the list to store the scraped data

    # Scraping Loop
    for i, url in enumerate(URLS):
        print(f"Scraping {i+1}/{len(URLS)}: {url}")
        page = requests.get(url, headers=HEADERS)
        
        # Check if the response status code is 200
        if page.status_code != 200:
            print(f"Failed to fetch {url}, status code: {page.status_code}.")
            continue

        try:
            soup = BeautifulSoup(page.text, 'html.parser')
            data = soup.find('div', {'class': 'QuoteStrip-dataContainer QuoteStrip-extendedHours'}).text
            title = soup.title.text

            # Extract fields
            company = re.search(pattern, title).group(1).strip()
            price = re.search(price_pattern, data).group(1)
            change = re.search(change_pattern, data).group(1)
            percentage = re.search(percentage_pattern, data).group(1)
            volume = re.search(volume_pattern, data)
            volume = volume.group(1).replace(',', '') if volume else "N/A"

            all_data.append([company, price, change, percentage, volume])

        except AttributeError as e:
            print(f"Failed to scrape data for {url}: {e}")
        
        # Wait for a random time between 5 to 15 seconds
        time.sleep(random.randint(5, 15))

    # Create the DataFrame
    column_names = ["Company", "Price", "Change", "Percentage", "Volume"]
    df = pd.DataFrame(all_data, columns=column_names)

    # Ensure the output directory exists
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    # Save to CSV in the raw data directory
    filename = f"{RAW_DATA_PATH}/raw_scraped_stocks_data.csv"
    df.to_csv(filename, index=False)
    print(f"Data scraping and saving completed successfully. File saved as {filename}.")


scrape_and_save()