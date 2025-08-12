import yfinance as yf
import streamlit as st
import pandas as pd

st.title("Stock Price Viewer")

st.write("This page allows the user to select specific assets (by typing their stock tickers) and visualize the prices and volumes traded for those assets over the chosen time period.")


# Input Data
st.write("### Select Parameters")
col1, col2 = st.columns(2)
assets = col1.text_input("Type the stock tickers here, separated by commas", "GOOGL, AAPL, MSFT")
start_date = col1.date_input("Start date",
                             value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(years=10),
                             min_value="1940-01-01",
                             max_value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(days=1))
end_date = col1.date_input("End date",
                           value="today",
                           min_value=start_date + pd.DateOffset(days=1),
                           max_value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(days=1)
                           )
ohlc = col2.selectbox("Open / High / Low / Close", ["Open", "High", "Low", "Close"], index=3)
frequency = col2.selectbox("Select the data frequency", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"])


data = yf.download(assets, start=start_date, end=end_date, interval=frequency)
prices = data[ohlc]

#ticker_data = yf.Ticker(ticker_symbol)
#ticker_df = ticker_data.history(period="5y", start=start_date, end=end_date)

st.write("## Price")
st.line_chart(prices)

st.write("## Volume")
st.line_chart(data.Volume)