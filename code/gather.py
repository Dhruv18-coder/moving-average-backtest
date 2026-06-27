import os
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

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
            multi_level_index = False
        )

        data.to_csv(filename)
        print(f"Saved data to {filename}")

    return data

ticker = "NVDA"
ticker_data = download(ticker)

print(f"{len(ticker_data)} rows loaded.")

plt.figure(figsize=(10, 5))
print(ticker_data.columns)
print(type(ticker_data.index))
print(ticker_data.dtypes)
plt.plot(ticker_data.index, ticker_data["Close"])
plt.title(f"{ticker} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)

plt.show()