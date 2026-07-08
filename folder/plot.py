import os
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)


def plot_strategy(df, ticker):
    plt.figure(figsize=(10, 5))

    plt.plot(df.index, df["BuyHold Value"], label="Buy & Hold")
    plt.plot(df.index, df["Strategy Value"], label="Moving Average Strategy")

    plt.title(f"{ticker} Comparing Strategy Results")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.legend()

    plt.savefig(f"charts/{ticker}_strategy.png", dpi=300)
    plt.show()


def plot_drawdown(buy_dd, strategy_dd, ticker):
    plt.figure(figsize=(10, 5))

    plt.plot(buy_dd.index, buy_dd, label="Buy & Hold Drawdown")
    plt.plot(strategy_dd.index, strategy_dd, label="Strategy Drawdown")

    plt.title(f"{ticker} Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.legend()

    plt.savefig(f"charts/{ticker}_drawdown.png", dpi=300)
    plt.show()