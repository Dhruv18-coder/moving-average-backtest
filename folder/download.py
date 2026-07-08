import os
import pandas as pd
import yfinance as yf

os.makedirs("data", exist_ok=True)


def download(ticker):
    filename = f"data/{ticker}_dailyprices.csv"

    if os.path.exists(filename):
        print(f"Loading cached data from {filename}")
        data = pd.read_csv(filename, index_col=0, parse_dates=True)
    else:
        print("Downloading data from Yahoo Finance...")
        data = yf.download(
            ticker,
            period="10y",
            interval="1d",
            auto_adjust=True,
            multi_level_index=False,
        )

        if not data.empty:
            data.to_csv(filename)

    if data.empty:
        raise ValueError(f"'{ticker}' is not a valid ticker symbol.")

    return data