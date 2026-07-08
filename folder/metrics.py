import pandas as pd


def calculate_metrics(df):
    result_values = pd.DataFrame(
        index=[
            "Total Return",
            "Annualized Return",
            "Volatility",
            "Sharpe Ratio",
            "Max Drawdown",
        ],
        columns=["Buy & Hold", "Moving Average Strategy"],
    )

    buy_return = df["BuyHold Value"].iloc[-1] - 1
    strategy_return = df["Strategy Value"].iloc[-1] - 1

    years = len(df) / 252

    buy_an_return = (df["BuyHold Value"].iloc[-1] ** (1 / years)) - 1
    strategy_an_return = (df["Strategy Value"].iloc[-1] ** (1 / years)) - 1

    buy_vol = df["Return"].std() * (252 ** 0.5)
    strategy_vol = df["Strategy Return"].std() * (252 ** 0.5)

    buy_sharpe = (
        (df["Return"].mean() / df["Return"].std()) * (252 ** 0.5)
        if buy_vol != 0
        else 0
    )

    strategy_sharpe = (
        (df["Strategy Return"].mean() / df["Strategy Return"].std()) * (252 ** 0.5)
        if strategy_vol != 0
        else 0
    )

    buy_dd = df["BuyHold Value"] / df["BuyHold Value"].cummax() - 1
    strategy_dd = df["Strategy Value"] / df["Strategy Value"].cummax() - 1

    buy_max_drawdown = buy_dd.min()
    strategy_max_drawdown = strategy_dd.min()

    result_values.loc["Total Return"] = [
        f"{buy_return:.2%}",
        f"{strategy_return:.2%}",
    ]

    result_values.loc["Annualized Return"] = [
        f"{buy_an_return:.2%}",
        f"{strategy_an_return:.2%}",
    ]

    result_values.loc["Volatility"] = [
        f"{buy_vol:.2%}",
        f"{strategy_vol:.2%}",
    ]

    result_values.loc["Sharpe Ratio"] = [
        f"{buy_sharpe:.2f}",
        f"{strategy_sharpe:.2f}",
    ]

    result_values.loc["Max Drawdown"] = [
        f"{buy_max_drawdown:.2%}",
        f"{strategy_max_drawdown:.2%}",
    ]

    return result_values, buy_dd, strategy_dd