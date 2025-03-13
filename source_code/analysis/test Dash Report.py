import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sqlite3
from config import DATABASE_PATH

# Step 1: Retrieve Data from SQLite
def retrieve_data(table="stock_pattern"):
    """Retrieve stock pattern data from SQLite database"""
    db_file_path = os.path.join(DATABASE_PATH, "stocks_database.db")
    try:
        conn = sqlite3.connect(db_file_path)
        data_df = pd.read_sql(f"SELECT * FROM {table}", conn)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
    
    return data_df

# Load dataset
df = retrieve_data("stock_pattern")

# Convert Date to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Compute additional KPIs
df['Daily_Return'] = df.groupby('Symbol')['Close'].pct_change()
df['Cumulative_Return'] = df.groupby('Symbol')['Daily_Return'].transform(lambda x: (1 + x).cumprod() - 1)
df['Volatility'] = df.groupby('Symbol')['Daily_Return'].rolling(30).std().reset_index(0, drop=True)

# Calculate Moving Averages
df['SMA_50'] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(50).mean())
df['EMA_20'] = df.groupby('Symbol')['Close'].transform(lambda x: x.ewm(span=20, adjust=False).mean())

# Identify Pattern Occurrences
df['Pattern'] = np.where(df['CDLDOJI'] == 1, 'Doji',
                np.where(df['CDLENGULFING'] == 1, 'Engulfing',
                np.where(df['CDLHAMMER'] == 1, 'Hammer', 'None')))

# Filter non-pattern data
pattern_df = df[df['Pattern'] != 'None']

# Create Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("📊 Stock Market Dashboard with Pattern Analysis", className="text-center mt-4"),

    # Stock selection dropdown
    dbc.Row([
        dbc.Col([
            html.Label("Select Stock:"),
            dcc.Dropdown(
                id="stock_selector",
                options=[{"label": stock, "value": stock} for stock in df['Symbol'].unique()],
                value=df['Symbol'].unique()[0],  # Default value
                multi=False
            )
        ], width=6)
    ], className="mb-4"),

    # First Row: Price Trend & Candlestick Chart (Side-by-Side)
    dbc.Row([
        dbc.Col(dcc.Graph(id='price_chart'), width=6),
        dbc.Col(dcc.Graph(id='candlestick_chart'), width=6),
    ], className="mb-4"),

    # Second Row: Pattern Pie Chart & Cumulative Returns (Side-by-Side)
    dbc.Row([
        dbc.Col(dcc.Graph(id='pattern_pie_chart'), width=6),
        dbc.Col(dcc.Graph(id='cumulative_return_chart'), width=6),
    ], className="mb-4"),

    # Third Row: Risk vs Return Chart (Full Width)
    dbc.Row([
        dbc.Col(dcc.Graph(id='risk_return_chart'), width=12),
    ], className="mb-4"),

    # Data Table
    html.H3("Stock Data Table"),
    dash_table.DataTable(
        id='stock_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'}
    )
])

# Callbacks to update visualizations
@app.callback(
    [
        dash.dependencies.Output('price_chart', 'figure'),
        dash.dependencies.Output('candlestick_chart', 'figure'),
        dash.dependencies.Output('cumulative_return_chart', 'figure'),
        dash.dependencies.Output('pattern_pie_chart', 'figure'),
        dash.dependencies.Output('risk_return_chart', 'figure')
    ],
    [dash.dependencies.Input('stock_selector', 'value')]
)
def update_charts(selected_stock):
    filtered_df = df[df['Symbol'] == selected_stock]
    filtered_patterns = pattern_df[pattern_df['Symbol'] == selected_stock]

    # **1️⃣ Stock Price Trend with Moving Averages**
    price_fig = px.line(filtered_df, x='Date', y='Close', title=f'{selected_stock} Stock Price')
    price_fig.add_scatter(x=filtered_df['Date'], y=filtered_df['SMA_50'], mode='lines', name='SMA 50', line=dict(dash='dot'))
    price_fig.add_scatter(x=filtered_df['Date'], y=filtered_df['EMA_20'], mode='lines', name='EMA 20', line=dict(dash='dash'))

    # Add markers for patterns
    for pattern in filtered_patterns['Pattern'].unique():
        pattern_data = filtered_patterns[filtered_patterns['Pattern'] == pattern]
        price_fig.add_scatter(x=pattern_data['Date'], y=pattern_data['Close'], 
                              mode='markers', name=pattern, marker=dict(size=10, symbol='circle-open'))

    # **2️⃣ Candlestick Chart with Volume**
    candlestick_fig = go.Figure(data=[
        go.Candlestick(
            x=filtered_df['Date'],
            open=filtered_df['Open'],
            high=filtered_df['High'],
            low=filtered_df['Low'],
            close=filtered_df['Close'],
            name="Candlestick"
        ),
        go.Bar(x=filtered_df['Date'], y=filtered_df['Volume'], name="Volume", marker=dict(color='rgba(50, 150, 255, 0.6)'))
    ])
    candlestick_fig.update_layout(title=f'{selected_stock} Candlestick & Volume', xaxis_rangeslider_visible=False)

    # **3️⃣ Cumulative Return Chart**
    return_fig = px.line(filtered_df, x='Date', y='Cumulative_Return', title=f'{selected_stock} Cumulative Returns')

    # **4️⃣ Pattern Frequency Pie Chart**
    pattern_counts = filtered_patterns['Pattern'].value_counts()
    pattern_pie_fig = px.pie(values=pattern_counts.values, names=pattern_counts.index,
                             title="Pattern Occurrence Frequency", color_discrete_sequence=px.colors.qualitative.Set3)

    # **5️⃣ Risk vs Return Scatter Plot**
    market_volatility = df.groupby('Symbol')['Volatility'].mean().reset_index()
    market_return = df.groupby('Symbol')['Daily_Return'].mean().reset_index()

    market_data = pd.merge(market_volatility, market_return, on="Symbol")
    
    selected_stock_data = market_data[market_data["Symbol"] == selected_stock]
    
    scatter_fig = px.scatter(
        market_data, x='Volatility', y='Daily_Return', text='Symbol',
        title=f"Risk vs Return: {selected_stock} vs Market",
        labels={"Volatility": "Risk (Volatility)", "Daily_Return": "Return (%)"},
        color='Volatility', size=np.abs(market_data['Daily_Return']) + 0.01,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    scatter_fig.add_trace(
        go.Scatter(
            x=selected_stock_data['Volatility'], 
            y=selected_stock_data['Daily_Return'],
            text=selected_stock_data['Symbol'],
            mode='markers',
            marker=dict(size=12, color='red', symbol="star"),
            name=f"{selected_stock} (Selected)"
        )
    )

    scatter_fig.update_traces(textposition='top center')

    return price_fig, candlestick_fig, return_fig, pattern_pie_fig, scatter_fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
