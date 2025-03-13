import os
import sqlite3
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
from pypfopt.plotting import plot_efficient_frontier, plot_weights
from config import DATABASE_PATH

def retrieve_data(table="full_stock_data"):
    """Retrieve stock data from SQLite database"""
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    try:
        conn = sqlite3.connect(db_file_path)
        print(f"Connected to database at: {db_file_path}")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        return None

    query = f"SELECT * FROM {table}"
    try:
        data_df = pd.read_sql(query, conn)
        print("Data retrieved successfully.")
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()
        print("Database connection closed.")

    return data_df

# Load stock data from the database
df = retrieve_data()

if df is not None:
    # Convert date column to datetime and sort data
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # **Ensure Close_pct_change is computed correctly**
    if 'Close_pct_change' not in df.columns:
        df['Close_pct_change'] = df.groupby('Symbol')['Close'].pct_change()

    # Assume risk-free rate of 2% annually, converted to daily
    risk_free_rate = 0.02 / 252

    # Calculate market return as the average return of all stocks
    market_return = df.groupby('Date')['Close_pct_change'].mean()

    # Prepare data for CAPM calculations
    capm_data = df.pivot(index='Date', columns='Symbol', values='Close_pct_change')

    # **Fix Issue**: Remove NaN and infinite values
    capm_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    capm_data.dropna(axis=1, thresh=int(0.90 * len(capm_data)), inplace=True)  # Keep stocks with >90% valid data
    capm_data.fillna(0, inplace=True)  # Fill remaining NaNs with 0

    if capm_data.empty:
        raise ValueError("No valid data available after cleaning! Check your stock data.")

    # Calculate beta for each stock
    betas = {}
    for symbol in capm_data.columns:
        X = market_return.loc[capm_data.index]  # Market returns
        y = capm_data[symbol]  # Stock returns

        X = sm.add_constant(X)  # Add intercept
        model = sm.OLS(y, X).fit()
        betas[symbol] = model.params[1]  # Beta coefficient

    # Calculate expected returns using CAPM formula
    expected_returns_capm = {
        symbol: risk_free_rate + betas[symbol] * (market_return.mean() - risk_free_rate)
        for symbol in betas
    }

    # Convert results to a DataFrame
    capm_results_df = pd.DataFrame.from_dict(expected_returns_capm, orient='index', columns=['Expected Return'])
    capm_results_df['Beta'] = capm_results_df.index.map(betas)

    # Save CAPM results to CSV
    capm_results_file = "capm_results.csv"
    capm_results_df.to_csv(capm_results_file)
    print(f"\nCAPM results saved to {capm_results_file}")

    # --- Modern Portfolio Theory (MPT) using PyPortfolioOpt ---
    
    # Compute Expected Returns & Covariance Matrix
    mu = expected_returns.mean_historical_return(capm_data)
    S = risk_models.sample_cov(capm_data)

    # **Fix 1: Remove Stocks with NaN Expected Returns**
    mu.dropna(inplace=True)
    capm_data = capm_data[mu.index]  # Keep only valid stocks
    S = S.loc[mu.index, mu.index]  # Align covariance matrix

    # **Fix 2: Normalize Covariance Matrix to Reduce Volatility Issues**
    S = S / np.max(np.abs(S))  # Normalize covariance matrix to avoid extreme values

    # **Fix 3: Winsorize Expected Returns to Remove Outliers**
    mu = mu.clip(lower=mu.quantile(0.05), upper=mu.quantile(0.95))

    # **Fix 4: Ensure Covariance Matrix is Positive Definite**
    try:
        min_eigenvalue = np.min(np.linalg.eigvals(S))
        if min_eigenvalue < 0:
            S += np.eye(len(S)) * (-min_eigenvalue + 1e-6)
    except np.linalg.LinAlgError:
        print("Covariance Matrix has issues. Replacing with identity matrix.")
        S = np.eye(len(S)) * 1e-6

    # **Portfolio Optimization**
    ef = EfficientFrontier(mu, S)

    try:
        weights = ef.max_sharpe(risk_free_rate=risk_free_rate, solver="SCS")
    except:
        print("Optimization failed. Switching to Minimum Volatility Portfolio.")
        try:
            weights = ef.min_volatility()
        except:
            raise ValueError("Optimization completely failed. Please check your dataset.")

    cleaned_weights = ef.clean_weights()
    expected_return, expected_volatility, expected_sharpe = ef.portfolio_performance()

    if np.isnan(expected_return) or np.isnan(expected_sharpe):
        raise ValueError("Optimization failed: Expected return or Sharpe Ratio is NaN. Check stock data.")

    # Save Optimized Portfolio Weights to CSV
    weights_df = pd.DataFrame.from_dict(cleaned_weights, orient='index', columns=['Weight'])
    weights_file = "optimized_portfolio_weights.csv"
    weights_df.to_csv(weights_file)
    print(f"\nOptimized portfolio weights saved to {weights_file}")

    # Save Portfolio Performance Metrics to CSV
    performance_data = {
        "Expected Return": [expected_return],
        "Expected Volatility": [expected_volatility],
        "Sharpe Ratio": [expected_sharpe]
    }
    performance_df = pd.DataFrame(performance_data)
    performance_file = "portfolio_performance.csv"
    performance_df.to_csv(performance_file, index=False)
    print(f"\nPortfolio performance metrics saved to {performance_file}")

    # **Print Outputs**
    print("\nFinal Optimized Portfolio Weights:")
    print(weights_df)

    print("\nFinal Portfolio Performance Metrics:")
    print(performance_df)

    # **Plot Efficient Frontier with Asset Names**
    ef_plot = EfficientFrontier(mu, S)  # New instance for plotting

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_efficient_frontier(ef_plot, ax=ax, show_assets=True)
    plt.title("Efficient Frontier with Asset Names")

    # **Add Labels for Each Asset**
    for i, symbol in enumerate(mu.index):
        risk = np.sqrt(S.iloc[i, i])  # Standard deviation (risk)
        ret = mu.iloc[i]  # Expected return
        ax.scatter(risk, ret, marker='o', s=50, label=symbol, alpha=0.7)  # Plot each stock
        ax.text(risk, ret, symbol, fontsize=9, ha='right', alpha=0.8)  # Annotate

    plt.xlabel("Risk (Standard Deviation)")
    plt.ylabel("Expected Return")
    plt.legend(fontsize=8, loc="best", frameon=True)  # Add legend
    plt.show()

    plot_weights(cleaned_weights)
