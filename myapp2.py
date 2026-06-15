import yfinance as yf
import pandas as pd
import streamlit as st


st.write("""
         # Stock Price App
         Shown below are the stock **closing price** and ***volume*** of Google and Apple
         """)

# Define the ticker symbols
tickerSymbol = "GOOGL"
tickerSymbol2 = "AAPL"

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
tickerData2 = yf.Ticker(tickerSymbol2)

# Get the historical prices for this ticker
tickerDf = tickerData.history(start='2016-6-10', end='2026-6-10')
tickerDf2 = tickerData2.history(period="10y")

# Open the data

st.write("""
         ## Google Stock Closing Price
         """)
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)

st.write("""
         ## Apple Stock Closing Price
         """)
st.bar_chart(tickerDf2.Close)
st.bar_chart(tickerDf2.Volume)

