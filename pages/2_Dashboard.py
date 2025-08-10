import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Portfolio Returns Calculator")

assets = st.text_input('Enter asset tickers separated by commas', "AAPL, MSFT, GOOGL")

start = st.date_input("Start date", value =pd.to_datetime('2022-05-01'))
end = st.date_input("End date", value=pd.to_datetime('2023-05-01'))

data = yf.download(assets, start=start, end=end, auto_adjust=False)['Adj Close']

ret_df = data.pct_change()
cum_ret = (ret_df + 1).cumprod() - 1
pf_cum_ret = cum_ret.mean(axis=1)

benchmark = yf.download('^GSPC', start=start, end=end, auto_adjust=False)['Adj Close']

bench_ret = benchmark.pct_change()
bench_dev = (bench_ret + 1).cumprod() - 1

W = (np.ones(len(ret_df.cov())) / len(ret_df.cov()))
pf_std = (W.dot(ret_df.cov()).dot(W)) ** (1/2)

st.subheader("Portfolio vs. Index Development")

tog = pd.concat([bench_dev, pf_cum_ret], axis=1)
tog.columns = ['S&P500', 'Portfolio Performance']

st.line_chart(data=tog)


st.subheader("Portfolio Risk")
pf_std

st.subheader("Benchmark Risk")
bench_risk = bench_ret.std()
bench_risk

st.subheader("Portfolio composition")
fig,ax = plt.subplots(facecolor='#121212')
ax.pie(W, labels=data.columns, autopct='%1.1%%', textprops={'color':'white'})
st.pyplot(fig)