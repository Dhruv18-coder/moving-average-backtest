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
            multi_level_index=False
        )

        if not data.empty:
            data.to_csv(filename)

    if data.empty:
        raise ValueError(f"'{ticker}' is not a valid ticker symbol.")

    return data

default_tickers = ["NVDA", "AAPL", "NFLX", "NNE", "AMZN"]

user_input = input(
    "Enter ticker symbols separated by commas (press Enter for defaults): "
).strip()

if user_input:
    tickers = [t.strip().upper() for t in user_input.split(",")]
else:
    tickers = default_tickers

for t in tickers:
    print(f"Results for ticker {t} are: ")
    try:
        ticker_data = download(t)
    except ValueError as e:
        print(e)
        continue


    ticker_data["MA20"] = ticker_data["Close"].rolling(window=20).mean()
    ticker_data["MA50"] = ticker_data["Close"].rolling(window=50).mean()

    cost = 0.001
    ticker_data["Position"] = (ticker_data["MA20"] > ticker_data["MA50"]).astype(int)
    ticker_data["Position"] = (ticker_data["Position"].shift(1).fillna(0))
    ticker_data["Trade"] = ticker_data["Position"].diff().abs().fillna(0)
    ticker_data["Return"] = ticker_data["Close"].pct_change().fillna(0)
    ticker_data["Strategy Return"] = (
    (ticker_data["Return"] * ticker_data["Position"]) - ticker_data["Trade"] * cost
    )
    ticker_data["Status"] = ticker_data["Position"].map({1: "in market",0: "in cash"})
    ticker_data["BuyHold Value"] = (1 + ticker_data["Return"]).cumprod()
    ticker_data["Strategy Value"] = (1 + ticker_data["Strategy Return"]).cumprod()


    result_values = pd.DataFrame(
        index = [
            "Total Return",
            "Annualized Return",
            "Volatility",
            "Sharpe Ratio",
            "Max Drawdown"
        ],
        columns = ["Buy & Hold", "Moving Average Strategy"]
    )

    buy_return = ticker_data["BuyHold Value"].iloc[-1] - 1
    strategy_return = ticker_data["Strategy Value"].iloc[-1] - 1

    years = len(ticker_data) / 252 # Approximate number of trading days in a year

    buy_an_return = (ticker_data["BuyHold Value"].iloc[-1] ** (1/years)) - 1
    strategy_an_return = (ticker_data["Strategy Value"].iloc[-1] ** (1/years)) - 1

    buy_vol = ticker_data["Return"].std() * (252 ** 0.5)
    strategy_vol = ticker_data["Strategy Return"].std() * (252 ** 0.5)

    buy_sharpe = (ticker_data["Return"].mean() / ticker_data["Return"].std()) * (252 ** 0.5) if buy_vol != 0 else 0
    strategy_sharpe = (ticker_data["Strategy Return"].mean() / ticker_data["Strategy Return"].std()) * (252 ** 0.5) if strategy_vol != 0 else 0

    buy_dd = ticker_data["BuyHold Value"] / ticker_data["BuyHold Value"].cummax() - 1
    strategy_dd = ticker_data["Strategy Value"] / ticker_data["Strategy Value"].cummax() - 1

    buy_max_drawdown = buy_dd.min()
    strategy_max_drawdown = strategy_dd.min()

    result_values.loc["Total Return", "Buy & Hold"] = f"{buy_return:.2%}"
    result_values.loc["Total Return", "Moving Average Strategy"] = f"{strategy_return:.2%}"
    result_values.loc["Annualized Return", "Buy & Hold"] = f"{buy_an_return:.2%}"
    result_values.loc["Annualized Return", "Moving Average Strategy"] = f"{strategy_an_return:.2%}"
    result_values.loc["Volatility", "Buy & Hold"] = f"{buy_vol:.2%}"
    result_values.loc["Volatility", "Moving Average Strategy"] = f"{strategy_vol:.2%}"
    result_values.loc["Sharpe Ratio", "Buy & Hold"] = f"{buy_sharpe:.2f}"
    result_values.loc["Sharpe Ratio", "Moving Average Strategy"] = f"{strategy_sharpe:.2f}"
    result_values.loc["Max Drawdown", "Buy & Hold"] = f"{buy_max_drawdown:.2%}"
    result_values.loc["Max Drawdown", "Moving Average Strategy"] = f"{strategy_max_drawdown:.2%}"

    print(result_values)
    print(f"{len(ticker_data)} rows loaded.")
    print("")

    plt.figure(figsize=(10, 5))
    print(ticker_data[["Close", "MA20", "MA50", "Status", "Strategy Value", "BuyHold Value"]].tail())
                        
    plt.plot(ticker_data.index, ticker_data["BuyHold Value"], label="Buy & Hold", color="blue")
    plt.plot(ticker_data.index, ticker_data["Strategy Value"], label="Moving Average Strategy", color="red")

    plt.legend()
    plt.title(f"{t} Comparing Strategy results")
    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.grid(True)

    plt.show()

    plt.figure(figsize=(10,5))

    plt.plot(ticker_data.index, buy_dd, label="Buy & Hold Drawdown")
    plt.plot(ticker_data.index, strategy_dd, label="Strategy Drawdown")

    plt.title(f"{t} Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.legend()

    plt.show()

    num_trades = ticker_data["Trade"].sum()
    print(f"Number of trades for {t}: {int(num_trades)}")
