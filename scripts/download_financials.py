"""
Download annual Revenue and Net Income for the 20 Group-20 companies (NSE).

Source: Yahoo Finance via yfinance (annual income statement).
Output:
  data/financials_long.csv   - tidy long format (company, cap, fy, revenue_cr, net_income_cr)
  data/financials_wide.csv   - revenue & net income pivoted by fiscal year
  data/raw/<TICKER>_income.csv - raw yfinance income statement per company

Notes:
- Indian fiscal years end 31-Mar. "FY2022" = year ending Mar-2022.
- Figures are converted to Rs Crore (1 crore = 10,000,000) for readability.
- Yahoo typically provides ~4 most-recent annual periods, which covers the
  actuals required by the assignment (FY2022, FY2023, FY2024, and FY2025 once filed).
"""

from __future__ import annotations

import os
import time
import pandas as pd
import yfinance as yf

CRORE = 1e7

# (assignment_symbol, market_cap_bucket, [yahoo symbols to try in order])
COMPANIES = [
    ("ULTRACEMCO", "Large", ["ULTRACEMCO.NS"]),
    ("SHREECEM",   "Large", ["SHREECEM.NS"]),
    ("GRASIM",     "Large", ["GRASIM.NS"]),
    ("AMBUJACEM",  "Large", ["AMBUJACEM.NS"]),
    ("ACC",        "Large", ["ACC.NS"]),
    ("DALBHARAT",  "Large", ["DALBHARAT.NS"]),
    ("RAMCOCEM",   "Large", ["RAMCOCEM.NS"]),
    ("JKLAKSHMI",  "Large", ["JKLAKSHMI.NS"]),
    ("BIRLACORPN", "Large", ["BIRLACORPN.NS"]),
    ("HEIDELBERG", "Large", ["HEIDELBERG.NS"]),
    ("JKCEMENT",   "Mid",   ["JKCEMENT.NS"]),
    ("ORIENTCEM",  "Mid",   ["ORIENTCEM.NS"]),
    ("PRISMCEM",   "Mid",   ["PRSMJOHNSN.NS", "PRISMCEM.NS"]),  # renamed Prism Johnson
    ("NCLIND",     "Mid",   ["NCLIND.NS"]),
    ("BURNPUR",    "Mid",   ["BURNPUR.NS", "BURNPURCE.BO"]),
    ("SOMANYCERA", "Small", ["SOMANYCERA.NS"]),
    ("CERA",       "Small", ["CERA.NS"]),
    ("HSIL",       "Small", ["HSIL.BO", "HSIL.NS"]),
    ("ASTRAL",     "Small", ["ASTRAL.NS"]),
    ("SUPREMEIND", "Small", ["SUPREMEIND.NS"]),
]

REVENUE_KEYS = ["Total Revenue", "Operating Revenue", "TotalRevenue"]
NETINCOME_KEYS = [
    "Net Income",
    "Net Income Common Stockholders",
    "Net Income Continuous Operations",
    "NetIncome",
]


def first_row(df: pd.DataFrame, keys: list[str]) -> pd.Series | None:
    for k in keys:
        if k in df.index:
            return df.loc[k]
    return None


def fetch_company(symbol: str, cap: str, candidates: list[str], raw_dir: str) -> pd.DataFrame:
    for sym in candidates:
        try:
            tk = yf.Ticker(sym)
            inc = tk.income_stmt  # annual, columns = period end dates
            if inc is None or inc.empty:
                continue
            inc.to_csv(os.path.join(raw_dir, f"{symbol}_income.csv"))

            rev = first_row(inc, REVENUE_KEYS)
            ni = first_row(inc, NETINCOME_KEYS)
            rows = []
            for col in inc.columns:
                fy = pd.Timestamp(col).year  # Indian FY label = calendar year of Mar period end
                rows.append(
                    {
                        "company": symbol,
                        "cap": cap,
                        "yahoo_symbol": sym,
                        "fy": fy,
                        "revenue_cr": (rev[col] / CRORE) if rev is not None and pd.notna(rev[col]) else None,
                        "net_income_cr": (ni[col] / CRORE) if ni is not None and pd.notna(ni[col]) else None,
                    }
                )
            out = pd.DataFrame(rows).sort_values("fy")
            print(f"[ok]   {symbol:11s} via {sym:14s} years {sorted(out['fy'].tolist())}")
            return out
        except Exception as e:  # noqa: BLE001
            print(f"[warn] {symbol} via {sym}: {e}")
        time.sleep(0.4)
    print(f"[FAIL] {symbol}: no data from {candidates}")
    return pd.DataFrame(
        [{"company": symbol, "cap": cap, "yahoo_symbol": None, "fy": None,
          "revenue_cr": None, "net_income_cr": None}]
    )


def main() -> None:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "data")
    raw_dir = os.path.join(data_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    frames = [fetch_company(sym, cap, cands, raw_dir) for sym, cap, cands in COMPANIES]
    long_df = pd.concat(frames, ignore_index=True)
    long_df.to_csv(os.path.join(data_dir, "financials_long.csv"), index=False)

    valid = long_df.dropna(subset=["fy"]).copy()
    valid["fy"] = valid["fy"].astype(int)
    rev_wide = valid.pivot_table(index=["cap", "company"], columns="fy", values="revenue_cr")
    ni_wide = valid.pivot_table(index=["cap", "company"], columns="fy", values="net_income_cr")
    with pd.ExcelWriter(os.path.join(data_dir, "financials.xlsx")) as xl:
        rev_wide.round(0).to_excel(xl, sheet_name="Revenue_Cr")
        ni_wide.round(0).to_excel(xl, sheet_name="NetIncome_Cr")
    rev_wide.round(0).to_csv(os.path.join(data_dir, "revenue_wide_cr.csv"))
    ni_wide.round(0).to_csv(os.path.join(data_dir, "netincome_wide_cr.csv"))

    print("\nRevenue (Rs Cr):")
    print(rev_wide.round(0).to_string())
    print("\nNet Income (Rs Cr):")
    print(ni_wide.round(0).to_string())
    print("\nSaved: data/financials_long.csv, revenue_wide_cr.csv, netincome_wide_cr.csv, financials.xlsx")


if __name__ == "__main__":
    main()
