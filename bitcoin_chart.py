import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Streamlit app title
st.title("Bitcoin Price Movement Chart")

# Function to fetch Bitcoin data
def fetch_bitcoin_data(period="1mo"):
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period=period)
    return data

# Function to create candlestick chart
def plot_candlestick(data):
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Bitcoin"
        )
    ])
    fig.update_layout(
        title="Bitcoin Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False
    )
    return fig

# Function to create line chart
def plot_line_chart(data):
    fig = go.Figure(data=[
        go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name="Closing Price",
            line=dict(color='blue')
        )
    ])
    fig.update_layout(
        title="Bitcoin Closing Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )
    return fig

# Sidebar for user input
st.sidebar.header("Chart Settings")
time_period = st.sidebar.selectbox(
    "Select Time Period",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd"],
    index=2  # Default to 1 month
)

# Fetch data
data = fetch_bitcoin_data(period=time_period)

# Display metrics
st.subheader("Bitcoin Price Overview")
col1, col2, col3 = st.columns(3)
latest_price = data['Close'][-1]
col1.metric("Latest Price", f"${latest_price:,.2f}")
price_change = ((data['Close'][-1] - data['Open'][0]) / data['Open'][0]) * 100
col2.metric("Price Change (%)", f"{price_change:.2f}%")
col3.metric("Volume (Latest)", f"{data['Volume'][-1]:,.0f}")

# Plot charts
st.subheader("Candlestick Chart")
st.plotly_chart(plot_candlestick(data), use_container_width=True)

st.subheader("Closing Price Trend")
st.plotly_chart(plot_line_chart(data), use_container_width=True)

# Display raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Bitcoin Data")
    st.dataframe(data)
