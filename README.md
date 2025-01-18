# **End-to-End Stock Market Analysis and Prediction**

## **Project Overview**

The End-to-End Stock Market Analysis and Prediction project seeks to provide a complete solution for evaluating and forecasting stock market data. 
This project combines a variety of data science techniques, including web scraping, exploratory data analysis (EDA), and predictive modeling with machine learning algorithms. The system gathers stock market data from several web sources, cleans and processes it, and then stores it in a PostgreSQL database for efficient querying. The project also uses interactive data visualizations like Plotly Dash and Power BI to provide consumers with dynamic and relevant information.
The project forecasts stock price fluctuations using machine learning techniques like KNN classification, which provides useful information for financial market decision-making.

------------------------------------------------------------------------

## **Features**

-   **Data Collection:** Scrape stock market data from online sources using BeautifulSoup.
-   **Data Wrangling:** Clean and process raw data for analysis and modeling.
-   **Database Integration:** Store processed data in a SQLite database.
-   **Exploratory Data Analysis:** Perform visual and SQL-based analyses of stock trends.
-   **Interactive Dashboards:** Create dynamic visualizations using Plotly Dash.
-   **Predictive Modeling:** Use machine learning (e.g., KNN classification) for stock price predictions.
-   **Power BI Integration:** Additional interactive visual analytics.

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
│
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
