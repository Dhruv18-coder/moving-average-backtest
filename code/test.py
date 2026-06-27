import yfinance as yf
import pandas as pd

def download(ticker):
    data = yf.download(ticker, period = "10y", interval = "1d", auto_adjust = True)
    return data

ticker = "AAPL"
ticker_data = download(ticker)

filename = f"data/{ticker}_dailyprices.csv"
ticker_data.to_csv(filename)

print(f"Downloaded {ticker} data to {len(ticker_data)} rows and saved to {filename}")

print(ticker_data.head())