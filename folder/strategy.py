def apply_strategy(df):
    cost = 0.001

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    df["Position"] = (df["MA20"] > df["MA50"]).astype(int)
    df["Position"] = df["Position"].shift(1).fillna(0)

    df["Trade"] = df["Position"].diff().abs().fillna(0)

    df["Return"] = df["Close"].pct_change().fillna(0)

    df["Strategy Return"] = (
        df["Return"] * df["Position"]
        - df["Trade"] * cost
    )

    df["Status"] = df["Position"].map(
        {1: "in market", 0: "in cash"}
    )

    df["BuyHold Value"] = (1 + df["Return"]).cumprod()
    df["Strategy Value"] = (1 + df["Strategy Return"]).cumprod()

    return df