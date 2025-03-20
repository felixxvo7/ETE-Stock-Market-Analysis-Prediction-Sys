import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error

from config import DATABASE_PATH 

# Retrieve Data from SQLite
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

# Preprocess Data
def preprocess_data(df, stock_symbol="AAPL", seq_length=90):
    """Prepares data for LSTM training with multiple features"""
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Symbol'] == stock_symbol].sort_values(by='Date')

    # Selecting features for training (Close, Volume, RSI, MACD)
    features = ['Close', 'Volume', 'RSI_14', 'MACD_12_26_9']
    df = df[['Date'] + features].set_index('Date')

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(df)

    # Create sequences
    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i : i + seq_length])
            y.append(data[i + seq_length, 0]) 
        return np.array(X), np.array(y)

    X, y = create_sequences(data_scaled, seq_length)

    # Split into training/testing sets
    train_size = int(len(X) * 0.8)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # Reshape inputs for LSTM (samples, timesteps, features)
    X_train = X_train.reshape((X_train.shape[0], seq_length, len(features)))
    X_test = X_test.reshape((X_test.shape[0], seq_length, len(features)))

    return X_train, y_train, X_test, y_test, scaler, df.index[-len(y_test):], features

# Build LSTM Model
def build_lstm_model(input_shape):
    """Defines and compiles an LSTM model"""
    model = Sequential([
        LSTM(100, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(100, return_sequences=False),
        Dropout(0.2),
        Dense(50, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train & Evaluate Model
def train_lstm(X_train, y_train, X_test, y_test, scaler, date_index, features):
    """Trains the LSTM model and evaluates it"""
    model = build_lstm_model((X_train.shape[1], len(features)))
    history = model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test), verbose=1)
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(
        np.concatenate([predictions, np.zeros((predictions.shape[0], len(features) - 1))], axis=1)
    )[:, 0] 

    actual_prices = scaler.inverse_transform(
        np.concatenate([y_test.reshape(-1, 1), np.zeros((y_test.shape[0], len(features) - 1))], axis=1)
    )[:, 0]  
    mse = mean_squared_error(actual_prices, predictions)
    mae = mean_absolute_error(actual_prices, predictions)
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(date_index, actual_prices, label="Actual Prices")
    plt.plot(date_index, predictions, label="Predicted Prices", linestyle="dashed")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(f"LSTM Stock Price Prediction ({features})")
    plt.legend()
    plt.show()

    return model

# Main execution
if __name__ == "__main__":
    df = retrieve_data()
    if df is not None:
        X_train, y_train, X_test, y_test, scaler, date_index, features = preprocess_data(df, stock_symbol="AAPL", seq_length=90)
        model = train_lstm(X_train, y_train, X_test, y_test, scaler, date_index, features)
