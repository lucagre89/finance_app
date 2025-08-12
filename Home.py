import yfinance as yf
import streamlit as st
import pandas as pd

st.title("An App to Visualize Financial Data")

st.write("This web app allows users to easily visualize financial data, such as: \n * prices and volumes traded over time for selected assets \n * returns over time for a user-specified portfolio")

st.write("The services are provided in dedicated pages, which can be accessed from the links below or from the sidebar menu.")

st.page_link("pages/1_📈_Stock_Prices_Viewer.py", label="**Stock Prices Viewer**", icon="📈", help="Link to the Stock Prices Viewer service")

st.page_link("pages/2_📊_Portfolio_Returns_Calculator.py", label="**Portfolio Returns Calculator**", icon="📊", help="Link to the Portfolio Returns Calculator service")

st.write("Libraries used: yfinance, pandas, matplotlib, streamlit")

