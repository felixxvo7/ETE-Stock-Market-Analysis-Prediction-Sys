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


def preprocess_data(data, sequence_length=60):
    """
    Preprocess the data for the LSTM model:
    - Normalize the data.
    - Create sequences of data.

    Parameters:
        data (pd.DataFrame): The stock data (must contain a 'Close' column).
        sequence_length (int): The length of the input sequences.

    Returns:
        tuple: (X_train, y_train, X_test, y_test, scaler)
    """
    # Extract the 'Close' column
    close_prices = data["Close"].values.reshape(-1, 1)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    # Create sequences
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i - sequence_length:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)

    # Reshape X to be compatible with LSTM input
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Split the data into training and testing sets
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    return X_train, y_train, X_test, y_test, scaler

def build_lstm_model(input_shape):
    """
    Build the LSTM model.

    Parameters:
        input_shape (tuple): The shape of the input data (sequence_length, 1).

    Returns:
        model: The compiled LSTM model.
    """
    model = Sequential()

    # First LSTM layer
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))

    # Second LSTM layer
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))

    # Dense output layer
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    return model

def train_model(model, X_train, y_train, X_test, y_test, epochs=50, batch_size=32):
    """
    Train the LSTM model.

    Parameters:
        model: The LSTM model.
        X_train, y_train: Training data.
        X_test, y_test: Validation data.
        epochs (int): Number of training epochs.
        batch_size (int): Batch size for training.

    Returns:
        history: Training history.
    """
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    return history

def validate_model(model, X_test, y_test, scaler):
    """
    Validate the LSTM model and calculate performance metrics.

    Parameters:
        model: The trained LSTM model.
        X_test, y_test: Testing data.
        scaler: The scaler used to normalize the data.

    Returns:
        tuple: (y_test_actual, y_test_predicted, mse, rmse, mae)
    """
    # Predict on the test data
    y_test_predicted = model.predict(X_test)

    # Inverse transform the predictions and actual values
    y_test_predicted = scaler.inverse_transform(y_test_predicted.reshape(-1, 1))
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Check for NaN and handle
    if np.isnan(y_test_actual).any() or np.isnan(y_test_predicted).any():
        raise ValueError("NaN values detected in validation data. Check preprocessing steps.")

    # Calculate performance metrics
    mse = mean_squared_error(y_test_actual, y_test_predicted)
    rmse = np.sqrt(mse)  # Calculate RMSE
    mae = mean_absolute_error(y_test_actual, y_test_predicted)

    return y_test_actual, y_test_predicted, mse, rmse, mae


def plot_results(y_test_actual, y_test_predicted, symbol):
    """
    Plot the actual vs. predicted stock prices.

    Parameters:
        y_test_actual (np.array): The actual stock prices.
        y_test_predicted (np.array): The predicted stock prices.
        symbol (str): The stock symbol (used for the plot title).
    """
    plt.figure(figsize=(14, 5))
    plt.plot(y_test_actual, color="blue", label=f"Actual {symbol} Price")
    plt.plot(y_test_predicted, color="red", label=f"Predicted {symbol} Price")
    plt.title(f"{symbol} Stock Price Prediction")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example: Use the stationary data for a specific symbol
    symbol = "AAPL"
    data = retrieve_data(table="stationary_data_all")  # Retrieve stationary data
    data = data[data["Symbol"] == symbol]  # Filter for the specific symbol

    # Preprocess the data
    X_train, y_train, X_test, y_test, scaler = preprocess_data(data)

    # Build the LSTM model
    model = build_lstm_model(input_shape=(X_train.shape[1], 1))

    # Train the model
    print("Training the LSTM model...")
    history = train_model(model, X_train, y_train, X_test, y_test, epochs=50, batch_size=32)

    # Validate the model
    print("Validating the LSTM model...")
    y_test_actual, y_test_predicted, mse, rmse, mae = validate_model(model, X_test, y_test, scaler)


    # Print performance metrics
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")

    # Plot the results
    plot_results(y_test_actual, y_test_predicted, symbol)