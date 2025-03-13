import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error

from config import DATABASE_PATH  # Ensure DATABASE_PATH is correctly set

# Step 1: Retrieve Data from SQLite
def retrieve_data(table="full_stock_data"):
    """Retrieve stock data from SQLite database"""
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    try:
        conn = sqlite3.connect(db_file_path)
        print(f"Connected to database at: {db_file_path}")
        data_df = pd.read_sql(f"SELECT * FROM {table}", conn)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

    return data_df

# Step 2: Preprocess Data for Multiple Stocks
def preprocess_data(df, seq_length=90):
    """Prepares data for LSTM training across multiple stocks"""

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Symbol', 'Date'])  # Ensure correct order

    # Features to use
    features = ['Close', 'Volume', 'RSI_14', 'MACD_12_26_9']
    
    # Encode stock symbols
    stock_encoder = OneHotEncoder(sparse_output=False)  # FIXED HERE
    stock_symbols = df[['Symbol']]
    stock_encoded = stock_encoder.fit_transform(stock_symbols)

    # Generate correct column names for one-hot encoding
    stock_labels = stock_encoder.categories_[0]  # List of unique stock symbols
    stock_column_names = [f"Symbol_{s}" for s in stock_labels]

    # Convert to DataFrame with correct column names
    stock_encoded_df = pd.DataFrame(stock_encoded, columns=stock_column_names, index=df.index)

    # Merge the encoded symbols back into the DataFrame
    df_encoded = pd.concat([df.reset_index(drop=True), stock_encoded_df], axis=1)

    # Select only relevant features + one-hot encoded stock symbols
    feature_cols = features + stock_column_names
    df_encoded = df_encoded[['Date', 'Symbol'] + feature_cols].set_index('Date')

    # Normalize each stock separately
    scalers = {}
    for stock in df['Symbol'].unique():
        scaler = MinMaxScaler(feature_range=(0, 1))
        stock_data = df_encoded[df_encoded['Symbol'] == stock][feature_cols]
        df_encoded.loc[df_encoded['Symbol'] == stock, feature_cols] = scaler.fit_transform(stock_data)
        scalers[stock] = scaler  # Store the scaler for inverse transform

    df_encoded.drop(columns=['Symbol'], inplace=True)  # Remove Symbol column

    # Create sequences
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i : i + seq_length])  # 90-day input window
            y.append(data[i + seq_length, 0])  # Predict 'Close' price (first column)
        return np.array(X), np.array(y)

    X, y = create_sequences(df_encoded.values, seq_length)

    # Split into training/testing sets
    train_size = int(len(X) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # Reshape inputs for LSTM (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], seq_length, len(feature_cols)))
    X_test = X_test.reshape((X_test.shape[0], seq_length, len(feature_cols)))

    return X_train, y_train, X_test, y_test, scalers, df_encoded.index[-len(y_test):], feature_cols, stock_encoder

# Step 3: Build LSTM Model for Multi-Stock Prediction
def build_lstm_model(input_shape):
    """Defines and compiles an LSTM model"""
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(100, return_sequences=False),
        Dropout(0.2),
        Dense(50, activation='relu'),
        Dense(1)  # Predicting Close price
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Step 4: Train & Evaluate Model
def train_lstm(X_train, y_train, X_test, y_test, scalers, date_index, feature_cols, stock_encoder):
    """Trains the LSTM model and evaluates it"""
    model = build_lstm_model((X_train.shape[1], len(feature_cols)))
    history = model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test), verbose=1)

    # Predictions
    predictions = model.predict(X_test)

    # Inverse transform predictions (per stock)
    decoded_stocks = stock_encoder.inverse_transform(X_test[:, -1, -stock_encoder.categories_[0].size:])
    predicted_prices = []
    actual_prices = []

    for i, stock in enumerate(decoded_stocks):
        stock_name = stock[0]
        scaler = scalers[stock_name]

        # Inverse scale only 'Close' prices
        pred = scaler.inverse_transform(
            np.concatenate([predictions[i].reshape(-1, 1), np.zeros((1, len(feature_cols) - 1))], axis=1)
        )[0, 0]
        
        actual = scaler.inverse_transform(
            np.concatenate([y_test[i].reshape(-1, 1), np.zeros((1, len(feature_cols) - 1))], axis=1)
        )[0, 0]

        predicted_prices.append(pred)
        actual_prices.append(actual)

    # Metrics
    mse = mean_squared_error(actual_prices, predicted_prices)
    mae = mean_absolute_error(actual_prices, predicted_prices)
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(date_index, actual_prices, label="Actual Prices")
    plt.plot(date_index, predicted_prices, label="Predicted Prices", linestyle="dashed")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(f"LSTM Multi-Stock Price Prediction ({len(stock_encoder.categories_[0])} Stocks)")
    plt.legend()
    plt.show()

    return model

# Main execution
if __name__ == "__main__":
    df = retrieve_data()
    if df is not None:
        X_train, y_train, X_test, y_test, scalers, date_index, feature_cols, stock_encoder = preprocess_data(df, seq_length=90)
        model = train_lstm(X_train, y_train, X_test, y_test, scalers, date_index, feature_cols, stock_encoder)
