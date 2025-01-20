# **End-to-End Stock Market Analysis and Prediction**

## **Project Overview**

The End-to-End Stock Market Analysis and Prediction project provides a complete solution for visualizing and forecasting stock market data. 

This project combines various data science techniques, including web scraping, data collection, data wrangling, data cleaning, exploratory data analysis (EDA), and predictive modelling with machine learning algorithms. 

The system gathers stock market data from several web sources and yfinance packages, cleans and processes it, and then stores it in a SQLite3 database for efficient querying. The project also uses interactive data visualizations like Plotly Dash and Power BI to provide consumers with dynamic and relevant information.

The project forecasts stock price fluctuations using machine learning techniques like KNN classification, which provides useful information for financial market decision-making. It will have an interactive visualization through Plotly Dash and PowerBI to observe and forecasting stock market data.

**This project is to be continued, the above features are the expected features that the project will have ideally in the future. However,  web scraping, data collection, data wrangling, data cleaning, and Database managing are ready to go. However, EDA and ML_model are implemented but might need further improvement(those are just scraps). The PowerBI exploration is based on the collected data, not from the EDA, and might require further updates. Stay tuned!!!**

------------------------------------------------------------------------

## **Features**

-   **Data Collection:** Scrape stock market data from online sources using BeautifulSoup.Or collected through yfinance.
-   **Data Wrangling:** Clean and process raw data for analysis and modelling.(Cleaning data by handling missing data, adding more columns that will support EDA after)
-   **Database Integration:** Store processed two tables of data in an SQLite database.
-   **Exploratory Data Analysis:** Perform visual and SQL-based analyses of stock trends.
-   **Interactive Dashboards:** Create dynamic visualizations using Plotly Dash.
-   **Predictive Modeling:** Use machine learning (e.g., KNN classification, Linear regression, Logistic Regression or Clustering/Classification,...) for stock price predictions.
-   **Power BI or Dash Integration:** Additional interactive visual analytics.

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
│   │   ├── eda.py            
│   │   ├── ml_models.py       
│   │   └── visualization.py   
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

## **Key Technologies**

-   **Python Libraries:**
    -   `BeautifulSoup`: Web scraping
    -   `pandas`: Data manipulation
    -   `sqlalchemy`: Database interaction
    -   `plotly`: Interactive visualizations
    -   `scikit-learn`: Machine learning
-   **Database:** sqlite
-   **Visualization Tools:** Plotly Dash, Power BI

------------------------------------------------------------------------
## Author
Felix Vo
-   Expand visualization capabilities in Power BI and Dash.

------------------------------------------------------------------------

## Author

Felix Vo
