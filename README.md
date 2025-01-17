# **End-to-End Stock Market Analysis and Prediction**

## **Project Overview**

This project is a comprehensive solution for collecting, analyzing, and visualizing stock market data. The system performs web scraping, exploratory data analysis (EDA), and predictive modeling using machine learning techniques to provide insights and forecasts for stock prices.

The project follows a structured data science pipeline, integrating PostgreSQL for data management, Power BI for additional visualization, and Plotly Dash for interactive analytics.

------------------------------------------------------------------------

## **Features**

-   **Data Collection:** Scrape stock market data from online sources using BeautifulSoup.
-   **Data Wrangling:** Clean and process raw data for analysis and modeling.
-   **Database Integration:** Store processed data in a PostgreSQL database.
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
│   ├── __init__.py            # Makes 'src' a package
│   ├── database/
│   │   ├── __init__.py        # Database submodule
│   │   ├── db_connection.py   # Handles database connection
│   │   └── db_queries.py      # Executes database queries
│   ├── scraping/
│   │   ├── __init__.py        # Scraping submodule
│   │   ├── web_scraper.py     # Web scraping logic
│   │   └── utils.py           # Helper functions for scraping
│   ├── analysis/
│   │   ├── __init__.py        # Analysis submodule
│   │   ├── eda.py             # Exploratory data analysis
│   │   ├── ml_models.py       # Machine learning models
│   │   └── visualization.py   # Visualization logic
│   └── config.py              # Configuration file
│
├── data/
│   ├── raw_data/              # Raw scraped data
│   └── processed_data/        # Cleaned and processed data
│
├── .env                       # Environment variables
├── .gitignore                 # Files to exclude from Git
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

------------------------------------------------------------------------

## **Setup Instructions**

### **1. Clone the Repository**

``` bash
git clone https://github.com/felixxvo02/stock_analysis_project.git
cd stock_analysis_project
```

### **2. Create and Activate a Virtual Environment**

``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

``` bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**

Create a `.env` file in the project root and add the following:

```         
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_analysis_db
```

### **5. Run the Application**

Start the Plotly Dash app:

``` bash
python src/dashboard.py
```

Access the app at <http://127.0.0.1:8050/>.

------------------------------------------------------------------------

## **Key Technologies**

-   **Python Libraries:**
    -   `BeautifulSoup`: Web scraping
    -   `pandas`: Data manipulation
    -   `sqlalchemy`: Database interaction
    -   `plotly`: Interactive visualizations
    -   `scikit-learn`: Machine learning
-   **Database:** PostgreSQL
-   **Visualization Tools:** Plotly Dash, Power BI

------------------------------------------------------------------------

## **Future Improvements**

-   Integrate additional stock data APIs for more comprehensive insights.
-   Implement advanced ML models (e.g., Random Forest, LSTM).
-   Add automated data updates with scheduling tools (e.g., `cron` or `APScheduler`).
-   Expand visualization capabilities in Power BI and Dash.

------------------------------------------------------------------------

## Author

Felix Vo

------------------------------------------------------------------------

## **License**

This project is licensed under the MIT License. See `LICENSE` for more details.
