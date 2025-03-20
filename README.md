---
editor_options: 
  markdown: 
    wrap: 72
---

# **End-to-End Stock Market Analysis and Prediction**

[![License:
MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python
3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Code Style:
Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**A data-driven pipeline for stock market forecasting, combining web
scraping, machine learning, and interactive dashboards.** \## **Project
Overview**

This project provides an end-to-end solution for analyzing and
predicting stock market trends. It integrates technical analysis,
quantitative modeling, and risk management to deliver actionable
insights for traders and investors.

Technical Analysis: Study price patterns and trends using candlestick
charts and technical indicators.

Quantitative Analysis: Forecast stock prices using machine learning
(e.g., LSTM) and optimize portfolios using Modern Portfolio Theory
(MPT).

Project pipelines: data collect -\> data cleaning -\> data wrangling -\>
preprocess EDA -\> database -\> technical analysis -\> stationary test
-\> lstm -\> camp/mpt -\> model validation

Data columns in databases: ['Date', 'Open', 'High', 'Low', 'Close',
'Volume', 'Symbol', 'Company', 'Close_pct_change', 'Volume_pct_change',
'SMA_7', 'EMA_30', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9',
'RSI_14', 'BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'BBB_20_2.0',
'BBP_20_2.0', 'ATRr_14']

------------------------------------------------------------------------

## **Features**

### Data Pipeline

-   **Automated Data Collection**:
    -   Web scraping with `BeautifulSoup` for fundamental data\
    -   Historical OHLC data via `yfinance` API\
-   **Data Processing**:
    -   Cleaning, normalization, and feature engineering\
    -   SQLite database integration with `SQLite3`

### Technical Analysis

-   **Price Charts**:
    -   Use candlestick charts to identify patterns (e.g., head &
        shoulders, double tops/bottoms).\
-   **Indicators**:
    -   **Trend**: Moving Averages (SMA, EMA), MACD.\
    -   **Momentum**: RSI (Relative Strength Index), Stochastic
        Oscillator.\
    -   **Volatility**: Bollinger Bands, Average True Range (ATR).
        **Pattern Detection**:\
        The code includes functions to detect specific candlestick
        patterns:
    -   **Doji**: Identified by the `detect_doji` function, indicating
        indecision in the market.
    -   **Engulfing Patterns**: Detected using the `detect_engulfing`
        function, which identifies bullish and bearish engulfing
        patterns.
    -   **Hammer**: Recognized by the `detect_hammer` function,
        indicating potential bullish reversals.

### Quantitative Analysis

-   **Time-Series Forecasting**:
    -   LSTM neural networks for stock price prediction.\
-   **Factor Models**:
    -   CAPM (Capital Asset Pricing Model) to assess risk-adjusted
        returns.\
-   **Portfolio Optimization**:
    -   Use Modern Portfolio Theory (MPT) to balance risk and return.

### Risk Management

-   **Position Sizing**:
    -   Risk only 1-2% of your portfolio per trade.\
-   **Stop-Loss**:
    -   Set stop-loss orders based on volatility (e.g., 2x ATR).\
-   **Diversification**:
    -   Avoid overexposure to a single sector or asset.

### Visualization

-   **Interactive Dashboards**:
    -   Real-time charts with Plotly Dash\
    -   Financial reporting in Power BI\
-   **Dynamic Reports**:
    -   SQL-driven exploratory analysis

------------------------------------------------------------------------

## **Project Structure**

```         
stock_analysis_project/
│
├── source_code/
│   ├── __init__.py
│   ├── preprocessing/
│   │   ├── __init__.py 
│   │   ├── web_scraper.py    
│   │   └── collect_data.py
│   │   └── data_cleaning.py
│   │   └── wrangling_data.py
│   │   └── database.py     
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── preprocessing_EDA.py  
│   │   ├── technique_analysis.py   
│   │   ├── stationary_test.py
│   │   └── LSTM.py
│   │   └── CAMP & MPT.py
│   │   └── risk_management.py   
│   └── config.py           
├── notebook/
│   ├── data_collect.ipynb
│   ├── eda_SQL.ipynb
│   ├── ml_models.ipynb
│   ├── dashboard_prototype.ipynb            
├── data/
│   ├── raw_data/
│   ├── database/ 
│   └── processed_data/
├── visualization/
│   ├── ACF-PACF/             
│   └── candlestick_stock_chart/          
│   └── plots/
├── .env                  
├── .gitignore          
├── requirements.txt      
└── README.md           
```

## Dashboard and report snapshot

![](result/Screenshot%202025-03-14%20135716.png)

![](images/clipboard-3515375824.png)

![](result/PowerBI%20shot%20(2).png)

![](images/clipboard-2972370001.png)

![](images/clipboard-2053545494.png)

|  |
|:-----------------------------------------------------------------------|
| \## Stock Market Dataset (2024-2025) |
| \### Overview This dataset contains **daily stock market data** for **82 unique companies** (e.g., AAPL, AMZN, TSLA, NVDA) from **March 11, 2024, to March 8, 2025**. It includes price metrics, trading volume, and technical indicators, making it ideal for financial analysis, algorithmic trading, or predictive modeling. |
| \### Key Features - **Date**: Daily trading dates. - **Price Data**: `Open`, `High`, `Low`, `Close`. - **Volume**: Daily trading volume. - **Symbol & Company**: Ticker symbols and company names. - **Technical Indicators**: - Moving Averages (`SMA_7`, `EMA_30`). - MACD (`MACD_12_26_9`, Histogram, Signal Line). - RSI (`RSI_14`). - Bollinger Bands (`BBL_20_2.0`, `BBM_20_2.0`, `BBU_20_2.0`, `BBB_20_2.0`, `BBP_20_2.0`). - Volatility (`ATRr_14`). - **Percentage Changes**: `Close_pct_change`, `Volume_pct_change`. |
| \### Dataset Snapshot |
| \| **Category** \| **Tools & Libraries** \| \|------------------\|------------------------------------------------------\| \| **Data Collection** \| ![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-ff69b4), ![yfinance](https://img.shields.io/badge/-yfinance-blue), ![requests](https://img.shields.io/badge/-requests-green) \| \| **Data Processing** \| ![pandas](https://img.shields.io/badge/-pandas-150458), ![numpy](https://img.shields.io/badge/-numpy-013243), ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-red) \| \| **Machine Learning** \| ![scikit-learn](https://img.shields.io/badge/-scikit--learn-orange), ![statsmodels](https://img.shields.io/badge/-statsmodels-blue) \| \| **Visualization** \| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75), ![Matplotlib](https://img.shields.io/badge/-Matplotlib-blue), ![Power BI](https://img.shields.io/badge/-Power_BI-F2C811) \| \| **Database** \| ![SQLite](https://img.shields.io/badge/-SQLite-003B57) \| |

## Author

Felix Vo
