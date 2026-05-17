from __future__ import annotations

import pandas as pd


def sma(series: pd.Series, window: int = 20) -> pd.Series:
    return series.rolling(window=window, min_periods=1).mean()


def ema(series: pd.Series, window: int = 20) -> pd.Series:
    return series.ewm(span=window, adjust=False).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff().fillna(0.0)
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean().replace(0, 1e-9)
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0):
    mid = sma(series, window)
    std = series.rolling(window=window, min_periods=1).std().fillna(0.0)
    upper = mid + (num_std * std)
    lower = mid - (num_std * std)
    return upper, lower


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["SMA_20"] = sma(out["Close"], 20)
    out["EMA_20"] = ema(out["Close"], 20)
    out["RSI_14"] = rsi(out["Close"], 14)
    out["BB_UPPER"], out["BB_LOWER"] = bollinger_bands(out["Close"], 20, 2.0)
    out = out.bfill().ffill()
    return out
