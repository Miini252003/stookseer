from __future__ import annotations

from functools import lru_cache

import pandas as pd
import yfinance as yf


@lru_cache(maxsize=64)
def _download_cached(ticker: str, days: int) -> pd.DataFrame:
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Ticker is required.")

    df = yf.download(symbol, period=f"{days}d", auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data found for ticker '{symbol}'.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    needed = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in needed if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {', '.join(missing)}")

    df = df[needed].dropna().copy()
    df.index = pd.to_datetime(df.index)
    return df


def fetch_stock_history(ticker: str, days: int = 365) -> pd.DataFrame:
    return _download_cached(ticker.strip().upper(), int(days)).copy()
