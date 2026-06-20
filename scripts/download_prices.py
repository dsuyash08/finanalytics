"""
Download daily closing prices for the 20 Group-20 companies.

Covers 1 Jan 2024 - 31 Dec 2024 (Q6 requirement) and is extended through
31 Dec 2025 so the LLM forecasts for Jan/Mar/Dec 2025 can be checked against
actuals.

Output:
  data/prices_2024.csv        - Date x Company close price matrix (2024 only)
  data/prices_2024_2025.csv   - Date x Company close price matrix (2024-2025)
  data/price_targets.csv      - actual close on/near 31-Jan-25, 31-Mar-25, 31-Dec-25
"""

from __future__ import annotations

import os
import pandas as pd
import yfinance as yf

SYMBOLS = {
    "ULTRACEMCO": "ULTRACEMCO.NS", "SHREECEM": "SHREECEM.NS", "GRASIM": "GRASIM.NS",
    "AMBUJACEM": "AMBUJACEM.NS", "ACC": "ACC.NS", "DALBHARAT": "DALBHARAT.NS",
    "RAMCOCEM": "RAMCOCEM.NS", "JKLAKSHMI": "JKLAKSHMI.NS", "BIRLACORPN": "BIRLACORPN.NS",
    "HEIDELBERG": "HEIDELBERG.NS", "JKCEMENT": "JKCEMENT.NS", "ORIENTCEM": "ORIENTCEM.NS",
    "PRISMCEM": "PRSMJOHNSN.NS", "NCLIND": "NCLIND.NS", "BURNPUR": "BURNPUR.NS",
    "SOMANYCERA": "SOMANYCERA.NS", "CERA": "CERA.NS", "HSIL": "HSIL.BO",
    "ASTRAL": "ASTRAL.NS", "SUPREMEIND": "SUPREMEIND.NS",
}


def asof_close(s: pd.Series, target: str) -> float | None:
    """Last available close on or before target date."""
    t = pd.Timestamp(target)
    sub = s[s.index <= t].dropna()
    return float(sub.iloc[-1]) if len(sub) else None


def main() -> None:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)

    raw = yf.download(
        list(SYMBOLS.values()), start="2024-01-01", end="2026-01-01",
        auto_adjust=False, progress=False,
    )
    close = raw["Close"].copy()
    # rename yahoo symbols back to assignment tickers
    inv = {v: k for k, v in SYMBOLS.items()}
    close.columns = [inv.get(c, c) for c in close.columns]
    close = close.reindex(columns=list(SYMBOLS.keys()))

    full = close.round(2)
    full.to_csv(os.path.join(data_dir, "prices_2024_2025.csv"))
    full.loc["2024-01-01":"2024-12-31"].to_csv(os.path.join(data_dir, "prices_2024.csv"))

    targets = pd.DataFrame({
        "close_31Jan2025": {c: asof_close(close[c], "2025-01-31") for c in close.columns},
        "close_31Mar2025": {c: asof_close(close[c], "2025-03-31") for c in close.columns},
        "close_31Dec2025": {c: asof_close(close[c], "2025-12-31") for c in close.columns},
        "close_31Dec2024": {c: asof_close(close[c], "2024-12-31") for c in close.columns},
    }).round(2)
    targets.to_csv(os.path.join(data_dir, "price_targets.csv"))

    print("Price target actuals (Rs):")
    print(targets.to_string())
    print("\nSaved: data/prices_2024.csv, prices_2024_2025.csv, price_targets.csv")


if __name__ == "__main__":
    main()
