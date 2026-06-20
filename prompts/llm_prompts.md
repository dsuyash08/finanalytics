# Ready-to-paste LLM prompts (Q1 & Q6)

LLM used: **(state the exact model you used, e.g. "ChatGPT — GPT-5, web browsing OFF")**

These prompts are designed so the LLM **forecasts** from the supplied statements
rather than recalling memorised actuals. Use the **same** wording for every
company and every year (only swap the company name / attached file). Capture a
screenshot of each query and response.

---

## Q1.1 — Baseline forecast from the 2021 annual report

> You are a sell-side equity research analyst. I am attaching the FY2021 annual
> report of **{COMPANY}** (an Indian company; fiscal year ends 31 March 2021).
>
> Using **only** the financial statements, management discussion and disclosures
> contained in this FY2021 report — and explicitly **without** using any
> knowledge of what actually happened after March 2021 — forecast the company's:
>   1. Total Revenue (Rs crore)
>   2. Net Income / Profit after Tax (Rs crore)
>
> for the next three fiscal years: **FY2022, FY2023, FY2024**.
>
> Treat this strictly as a forward projection. Do not retrieve or recall actual
> reported figures for those years; derive them from FY2021 fundamentals.
>
> Show your working: state the FY2021 base revenue and net income you read from
> the report, the revenue growth rate and net-margin assumptions you apply for
> each year, and a brief justification (demand outlook, capacity, input costs,
> leverage) grounded in the report. Then present a table:
>
> | Year | Revenue (Rs cr) | Net Income (Rs cr) | Implied EPS (Rs) |
>
> If EPS is requested, use the share count disclosed in the FY2021 report.

Repeat for **2022 report** (predict FY2023, FY2024, FY2025), same wording with
"FY2021"→"FY2022" and the horizon years shifted by one.

---

## Q3 — Improved strategy (apply identically to ALL companies & years)

Chosen alternate strategy: **provide the trailing trend + an explicit
decomposition prompt** (revenue driven by volume×price, margin reversion to a
stated band). Keep this wording fixed across the panel.

> You are an equity research analyst forecasting **{COMPANY}**. I am attaching
> the FY{BASE} annual report. In addition, here are the company's last 4 years of
> reported figures from the report's historical columns:
>
> Revenue (Rs cr): {y-3}, {y-2}, {y-1}, {BASE}
> Net profit (Rs cr): {y-3}, {y-2}, {y-1}, {BASE}
>
> Forecast Revenue and Net Income for the next three fiscal years using this
> explicit method, and show each step:
> 1. Compute the 3-year revenue CAGR from the history above.
> 2. Project revenue for each future year = prior year × (1 + g), where g is the
>    CAGR adjusted for the demand commentary in the MD&A (state any adjustment).
> 3. Compute the average net margin over the last 3 years; assume the future net
>    margin reverts toward this 3-year average. State the margin used per year.
> 4. Net income = projected revenue × projected margin.
>
> Do not use any post-FY{BASE} actuals. Present the same table as before.

---

## Q4 — Earnings-surprise signal (per company, per result announcement)

> Using your forecast, compute an earnings surprise:
> Earnings Surprise = (Actual EPS − Forecast EPS) / (stock price 5 trading days
> before the earnings announcement date).
> I will supply the actual EPS, the announcement date, and the close price 5 days
> prior. Classify the surprise as positive/negative and tell me the buy-and-hold
> return you would earn by buying at the open of day +1 and holding to day +5.

(The actual return computation is done in `scripts/analyze.py`; the LLM step is
only for narrative interpretation.)

---

## Q6 — Stock-price forecast from 2024 daily closes

> You are a quantitative analyst. Attached is the daily closing price series for
> **{COMPANY}** from 1 January 2024 to 31 December 2024 (NSE). Using only this
> 2024 price history — and without recalling any actual 2025 prices — forecast
> the closing price on:
>   a) 31 January 2025
>   b) 31 March 2025
>   c) 31 December 2025
>
> State the method you use (trend, drift, momentum, mean reversion), the implied
> annualised drift and volatility from the 2024 data, and give a point estimate
> plus a direction (up/down vs the 31-Dec-2024 close) for each date. Present:
>
> | Target date | Forecast close (Rs) | Direction vs 31-Dec-2024 |

Run this with **identical** wording for all 20 tickers.
