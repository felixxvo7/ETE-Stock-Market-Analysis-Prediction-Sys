# **End-to-End Stock Market Analysis and Prediction**
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**A data-driven pipeline for stock market forecasting, combining web scraping, machine learning, and interactive dashboards.**
## **Project Overview**

This project provides an end-to-end solution for analyzing and predicting stock market trends. It integrates technical analysis, quantitative modeling, and risk management to deliver actionable insights for traders and investors.

Technical Analysis: Study price patterns and trends using candlestick charts and technical indicators.

Quantitative Analysis: Forecast stock prices using machine learning (e.g., LSTM) and optimize portfolios using Modern Portfolio Theory (MPT).

Risk Management: Implement position sizing, stop-loss strategies, and diversification to minimize risk.

------------------------------------------------------------------------

## **Features**

### Data Pipeline
- **Automated Data Collection**:  
  - Web scraping with `BeautifulSoup` for fundamental data  
  - Historical OHLC data via `yfinance` API  
- **Data Processing**:  
  - Cleaning, normalization, and feature engineering  
  - SQLite database integration with `SQLAlchemy`  

### Technical Analysis
- **Price Charts**:  
  - Use candlestick charts to identify patterns (e.g., head & shoulders, double tops/bottoms).  
- **Indicators**:  
  - **Trend**: Moving Averages (SMA, EMA), MACD.  
  - **Momentum**: RSI (Relative Strength Index), Stochastic Oscillator.  
  - **Volatility**: Bollinger Bands, Average True Range (ATR).  
- **Volume Analysis**:  
  - Rising volume confirms trends; declining volume signals weak trends.  

### Quantitative Analysis
- **Time-Series Forecasting**:  
  - LSTM neural networks for stock price prediction.  
- **Factor Models**:  
  - CAPM (Capital Asset Pricing Model) to assess risk-adjusted returns.  
- **Portfolio Optimization**:  
  - Use Modern Portfolio Theory (MPT) to balance risk and return.  

### Risk Management
- **Position Sizing**:  
  - Risk only 1-2% of your portfolio per trade.  
- **Stop-Loss**:  
  - Set stop-loss orders based on volatility (e.g., 2x ATR).  
- **Diversification**:  
  - Avoid overexposure to a single sector or asset.  

### Visualization
- **Interactive Dashboards**:  
  - Real-time charts with Plotly Dash  
  - Financial reporting in Power BI  
- **Dynamic Reports**:  
  - SQL-driven exploratory analysis  


------------------------------------------------------------------------

## **Project Structure**

```         
stock_analysis_project/
│
├── src/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py
│   │ 
│   ├── scraping/
│   │   ├── __init__.py 
│   │   ├── web_scraper.py    
│   │   └── collect_data.py
│   │   └── wrangling_data.py      
│   ├── analysis/
│   │   ├── __init__.py      
│   │   ├── technique_analysis.py   
│   │   ├── quantitative_analysis.py
│   │   └── risk_management.py   
│   └── config.py           
├── notebook/
│   ├── data_collect.ipynb
│   ├── eda_SQL.ipynb
│   ├── ml_models.ipynb
│   ├── dashboard_prototype.ipynb            
├── data/
│   ├── raw_data/             
│   └── processed_data/
├── PowerBI/
|
├── .env                  
├── .gitignore          
├── requirements.txt      
└── README.md           
```

------------------------------------------------------------------------

## Key Technologies

| **Category**         | **Tools & Libraries**                                              |
|----------------------|---------------------------------------------------------------------|
| **Data Collection**  | ![BeautifulSoup](https://img.shields.io/badge/-BeautifulSoup-ff69b4), ![yfinance](https://img.shields.io/badge/-yfinance-blue), ![requests](https://img.shields.io/badge/-requests-green) |
| **Data Processing**  | ![pandas](https://img.shields.io/badge/-pandas-150458), ![numpy](https://img.shields.io/badge/-numpy-013243), ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-red) |
| **Machine Learning** | ![scikit-learn](https://img.shields.io/badge/-scikit--learn-orange), ![statsmodels](https://img.shields.io/badge/-statsmodels-blue) |
| **Visualization**    | ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75), ![Matplotlib](https://img.shields.io/badge/-Matplotlib-blue), ![Power BI](https://img.shields.io/badge/-Power_BI-F2C811) |
| **Database**         | ![SQLite](https://img.shields.io/badge/-SQLite-003B57)             |

------------------------------------------------------------------------
## Author
Felix Vo
