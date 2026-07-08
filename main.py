from folder.download import download
from folder.strategy import apply_strategy
from folder.metrics import calculate_metrics
from folder.plot import plot_strategy, plot_drawdown

default_tickers = ["NVDA", "AAPL", "NFLX", "NNE", "AMZN"]

user_input = input(
    "Enter ticker symbols separated by commas (press Enter for defaults): "
).strip()

if user_input:
    tickers = [t.strip().upper() for t in user_input.split(",")]
else:
    tickers = default_tickers

for ticker in tickers:
    print(f"\nResults for ticker {ticker}")

    try:
        ticker_data = download(ticker)
    except ValueError as e:
        print(e)
        continue

    ticker_data = apply_strategy(ticker_data)

    results, buy_dd, strategy_dd = calculate_metrics(ticker_data)

    print(results)
    print(f"\n{len(ticker_data)} rows loaded.\n")

    print(
        ticker_data[
            [
                "Close",
                "MA20",
                "MA50",
                "Status",
                "Strategy Value",
                "BuyHold Value",
            ]
        ].tail()
    )

    plot_strategy(ticker_data, ticker)
    plot_drawdown(buy_dd, strategy_dd, ticker)

    print(f"\nNumber of trades for {ticker}: {int(ticker_data['Trade'].sum())}")