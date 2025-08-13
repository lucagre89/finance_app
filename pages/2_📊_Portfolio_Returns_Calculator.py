import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Portfolio Returns Calculator")

st.write("This page allows the user to specify the composition of a financial portfolio by selecting individual assets (and their relative share within the portfolio), and track its performance over the chosen time period. \n\n " \
"The user can also select a specific asset to use as a benchmark (e.g. the S&P500, or another index).")

number_inputs = st.number_input('Select number of assets in portfolio', step=1, min_value=1)
st.write('Number of assets: ', number_inputs)

col1, col2 = st.columns(2)

assets = [col1.text_input(f'Asset {i+1}', placeholder="Type asset ticker here", key=f"text_input_{i}")
          for i in range(number_inputs)]
weights_raw = [col2.number_input(f'% allocation for asset {i+1}', min_value=0, value=round(100/number_inputs), max_value=100, key=f"shares_{i}")
          for i in range(number_inputs)]
start_date = col1.date_input("Start date",
                             value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(years=10),
                             min_value="1940-01-01",
                             max_value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(days=1))
end_date = col2.date_input("End date",
                           value="today",
                           min_value=start_date + pd.DateOffset(days=1),
                           max_value=pd.to_datetime(pd.Timestamp.today()) - pd.DateOffset(days=1)
                           )
benchmark_asset = st.text_input('Select a benchmark ticker for comparison', value='^GSPC')

# Calculations
if assets[0] == '' or assets[-1] == '':
    pass
elif sum(weights_raw) > 100:
    st.error("Please make sure that the asset allocations sum to 100", icon=None, width="stretch")
else:

    # Rescale weights to shares in 0-1
    weights = [x/100 for x in weights_raw]
    # weights = []
    # for element in weights_raw:
    #     weights.append(element/100)

    # Import data
    prices = yf.download(assets, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
    benchmark = yf.download(benchmark_asset, start=start_date, end=end_date, auto_adjust=False)['Adj Close']

    # Portfolio returns calculation
    returns_df = prices.pct_change()

    portfolio_temp = []
    for asset in assets:
        portfolio_temp.append(returns_df[asset] * weights[assets.index(asset)])

    portfolio_returns = pd.concat(portfolio_temp, axis=1).sum(axis=1)
    returns_for_matrix = pd.DataFrame(pd.concat(portfolio_temp, axis=1)) # used for covariance matrix
    portfolio_returns.iloc[0] = np.nan
    portfolio_cum = (1 + portfolio_returns).cumprod() - 1

    # Benchmark returns calculation
    bench_ret = benchmark.pct_change()
    bench_cum = (bench_ret + 1).cumprod() - 1
    bench_risk = bench_ret.std()

    # Portfolio composition chart
    fig, ax = plt.subplots()
    ax.pie(weights, labels=assets, autopct='%1.1f%%')

    # Assets covariance matrix
    cov_matrix = returns_df.cov()
    W = np.array(weights)
    portfolio_std = (W.dot(returns_for_matrix.cov()).dot(W)) ** (1/2)

    # Plotting returns
    st.subheader("Portfolio vs. Benchmark performance")
    all = pd.concat([portfolio_cum, bench_cum], axis=1)
    all.columns = ['Portfolio', 'Benchmark']
    st.line_chart(data=all)

    # Display standard deviations
    data_container = st.container()
    with data_container:
        first, second = st.columns(2)
        with first:
            st.subheader("Portfolio composition")
            st.pyplot(fig)
        with second:
            st.subheader("Covariance of Returns")
            st.table(cov_matrix)

    data_container = st.container()
    with data_container:
        first, second = st.columns(2)
        with first:
            st.subheader("Portfolio StDev")
            st.text(portfolio_std)
        with second:
            st.subheader("Benchmark StDev")
            st.table(bench_risk)
    