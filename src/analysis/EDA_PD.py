import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import CLEANED_DATA_PATH

# Connect to SQLite database
def load_data_from_db(db_name='stocks_data.db', table_name='scraped_stock_data'):

    db_file_path = os.path.join(CLEANED_DATA_PATH, db_name)
    conn = sqlite3.connect(db_file_path)

    # Load the data into a pandas DataFrame
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    
    # Close the connection
    conn.close()

    return df

# Perform EDA
def perform_eda(df):
    # Show basic information about the data
    print("Data Information:")
    print(df.info())
    print("\n")

    # Show summary statistics for numerical columns
    print("Summary Statistics:")
    print(df.describe())
    print("\n")

    # Check for missing values
    print("Missing Values:")
    print(df.isnull().sum())
    print("\n")

    # Show the first few rows of the data
    print("First 5 rows of the data:")
    print(df.head())

    # Plot distributions of numerical columns
    plt.figure(figsize=(12, 6))
    df['price'].plot(kind='hist', bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Price Distribution')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()

    df['volume'].plot(kind='hist', bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
    plt.title('Volume Distribution')
    plt.xlabel('Volume')
    plt.ylabel('Frequency')
    plt.show()

    # Boxplot to check for outliers in 'price' and 'volume'
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[['price', 'volume']], orient='h')
    plt.title('Boxplot of Price and Volume')
    plt.show()

    # Correlation heatmap between numerical columns
    plt.figure(figsize=(10, 6))
    correlation_matrix = df[['price', 'volume']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

    # Scatter plot for price vs. volume
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='price', y='volume', data=df)
    plt.title('Price vs. Volume')
    plt.xlabel('Price')
    plt.ylabel('Volume')
    plt.show()

df = load_data_from_db()  # Load data from database
perform_eda(df)  # Perform EDA on the data

