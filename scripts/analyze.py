"""
Compute accuracy metrics once the LLM forecasts are filled in.

You paste the LLM's predictions into:
  inputs/forecasts_earnings.csv   (revenue / net income / EPS forecasts)
  inputs/forecasts_prices.csv     (stock price forecasts for Q6)

This script then computes the percentage difference vs the downloaded actuals
using the assignment formula:
    Percentage Difference = (Actual - Predicted) / Actual * 100

and aggregates accuracy by cap bucket and by forecast horizon. It also provides
a buy-and-hold return helper for the Q4 earnings-surprise signal.

Run:  py scripts/analyze.py
"""

from __future__ import annotations

import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
INPUTS = os.path.join(BASE, "inputs")


def pct_diff(actual: float, predicted: float) -> float | None:
    if actual in (None, 0) or pd.isna(actual) or pd.isna(predicted):
        return None
    return (actual - predicted) / actual * 100.0


# ---------------------------------------------------------------- earnings ---
def earnings_accuracy() -> None:
    f = os.path.join(INPUTS, "forecasts_earnings.csv")
    if not os.path.exists(f):
        print("[skip] inputs/forecasts_earnings.csv not found - fill the template first.")
        return

    fc = pd.read_csv(f)  # company, cap, base_year, metric, target_year, predicted
    rev = pd.read_csv(os.path.join(DATA, "revenue_wide_cr.csv"))
    ni = pd.read_csv(os.path.join(DATA, "netincome_wide_cr.csv"))

    def actual(metric: str, company: str, year: int) -> float | None:
        tbl = rev if metric.lower().startswith("rev") else ni
        row = tbl[tbl["company"] == company]
        col = str(year)
        if row.empty or col not in tbl.columns:
            return None
        v = row.iloc[0][col]
        return None if pd.isna(v) else float(v)

    fc["actual"] = [actual(m, c, y) for m, c, y in zip(fc["metric"], fc["company"], fc["target_year"])]
    fc["pct_diff"] = [pct_diff(a, p) for a, p in zip(fc["actual"], fc["predicted"])]
    fc["abs_pct"] = fc["pct_diff"].abs()
    fc["horizon"] = fc["target_year"] - fc["base_year"]

    fc.to_csv(os.path.join(INPUTS, "earnings_scored.csv"), index=False)
    print("\n=== Earnings forecast accuracy (MAPE %) ===")
    print("By cap bucket:")
    print(fc.groupby("cap")["abs_pct"].mean().round(1).to_string())
    print("\nBy horizon (years ahead):")
    print(fc.groupby("horizon")["abs_pct"].mean().round(1).to_string())
    print("\nBy cap x horizon:")
    print(fc.pivot_table(index="cap", columns="horizon", values="abs_pct", aggfunc="mean").round(1).to_string())
    print("\nSaved per-row scores: inputs/earnings_scored.csv")


# ------------------------------------------------------------------ prices ---
def price_accuracy() -> None:
    f = os.path.join(INPUTS, "forecasts_prices.csv")
    if not os.path.exists(f):
        print("\n[skip] inputs/forecasts_prices.csv not found - fill the template first.")
        return

    fc = pd.read_csv(f)  # company, target (jan/mar/dec), predicted
    tgt = pd.read_csv(os.path.join(DATA, "price_targets.csv"), index_col=0)
    colmap = {"jan": "close_31Jan2025", "mar": "close_31Mar2025", "dec": "close_31Dec2025"}
    base_col = "close_31Dec2024"

    def lookup(company: str, col: str) -> float | None:
        if company not in tgt.index or col not in tgt.columns:
            return None
        v = tgt.loc[company, col]
        return None if pd.isna(v) else float(v)

    rows = []
    for _, r in fc.iterrows():
        col = colmap.get(str(r["target"]).lower())
        actual = lookup(r["company"], col)
        base = lookup(r["company"], base_col)
        pred = r["predicted"]
        dir_actual = None if (actual is None or base is None) else (actual >= base)
        dir_pred = None if (pred is None or base is None) else (pred >= base)
        rows.append({
            "company": r["company"], "target": r["target"], "predicted": pred,
            "actual": actual, "base_31Dec2024": base,
            "direction_correct": (dir_actual == dir_pred) if None not in (dir_actual, dir_pred) else None,
            "pct_diff": pct_diff(actual, pred),
        })
    out = pd.DataFrame(rows)
    out["abs_pct"] = out["pct_diff"].abs()
    out.to_csv(os.path.join(INPUTS, "prices_scored.csv"), index=False)
    print("\n=== Stock-price forecast accuracy ===")
    print("Directional hit-rate by target:")
    print(out.groupby("target")["direction_correct"].mean().round(2).to_string())
    print("\nMean abs % error by target:")
    print(out.groupby("target")["abs_pct"].mean().round(1).to_string())
    print("\nSaved per-row scores: inputs/prices_scored.csv")


# ------------------------------------------------ Q4 buy-and-hold helper ----
def buy_and_hold(company: str, announce_date: str, hold_days: int = 5) -> float | None:
    """Buy at open of day +1 after the announcement, hold to day +hold_days; return %."""
    prices = pd.read_csv(os.path.join(DATA, "prices_2024_2025.csv"), index_col=0, parse_dates=True)
    if company not in prices.columns:
        return None
    s = prices[company].dropna()
    after = s[s.index > pd.Timestamp(announce_date)]
    if len(after) < hold_days + 1:
        return None
    buy = after.iloc[0]
    sell = after.iloc[hold_days]
    return (sell / buy - 1.0) * 100.0


if __name__ == "__main__":
    earnings_accuracy()
    price_accuracy()
    print("\nQ4 example (edit dates):",
          "ULTRACEMCO around 2024-04-25 ->",
          buy_and_hold("ULTRACEMCO", "2024-04-25"))
