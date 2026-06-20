# Using LLMs for Reasoning and Prediction — Group 20

**Sector note:** All 20 names in Group 20 are **cement / building-materials**
companies, so cross-company differences are driven mainly by size (cap bucket)
and balance-sheet strength rather than by industry. This makes the large- vs
mid- vs small-cap comparison in Q2 cleaner.

**LLM used:** _State the exact model and settings here, e.g. "ChatGPT (GPT-5),
browsing OFF, one fresh chat per company."_ Paste screenshots of each query and
response into `screenshots/` and reference them inline.

**Company universe**

| Bucket | Companies |
|---|---|
| Large-cap (10) | ULTRACEMCO, SHREECEM, GRASIM, AMBUJACEM, ACC, DALBHARAT, RAMCOCEM, JKLAKSHMI, BIRLACORPN, HEIDELBERG |
| Mid-cap (5) | JKCEMENT, ORIENTCEM, PRISMCEM (Prism Johnson), NCLIND, BURNPUR |
| Small-cap (5) | SOMANYCERA, CERA, HSIL, ASTRAL, SUPREMEIND |

> Reproducibility: every number below comes from scripts in `scripts/`.
> `download_financials.py` pulls annual revenue / net income, `download_prices.py`
> pulls 2024–2025 daily closes, and `analyze.py` scores the LLM forecasts you
> paste into `inputs/`. Annual-report PDFs (FY2021 & FY2022) are linked from each
> company's screener.in "Documents → Annual reports" section and on BSE.

---

## Remaining steps to finish (checklist)

Status legend: ✅ done (automated) · ⏳ needs an LLM session / your judgement.

**Already complete (no action needed):**

- ✅ **Source reports downloaded.** All 38 annual-report PDFs are in `reports/`
  as `<COMPANY>_FY2021.pdf` / `<COMPANY>_FY2022.pdf`. (ACC & AMBUJACEM have FY2021
  only — see note under "How to run"; that is the full obtainable set.)
- ✅ **Actuals downloaded.** Annual revenue/PAT (`data/revenue_wide_cr.csv`,
  `netincome_wide_cr.csv`, `financials.xlsx`) and daily prices 2021–2025
  (`data/prices_daily.csv`, `prices_2024.csv`, `price_targets.csv`).
- ✅ **Fixed prompts** for Q1/Q3/Q4/Q6 in `prompts/llm_prompts.md`.
- ✅ **Scoring pipeline** (`scripts/analyze.py`) and all input templates in
  `inputs/`.

**Left to do (each needs the LLM and your input):**

1. ⏳ **Pick & record the LLM** at the top of this report (model + settings).
2. ⏳ **Q1 earnings forecasts.** For each of the 20 companies, open a *fresh* chat,
   attach `reports/<COMPANY>_FY2021.pdf`, paste the Q1.1 prompt from
   `prompts/llm_prompts.md`, and screenshot the response. Repeat with
   `reports/<COMPANY>_FY2022.pdf` (horizon shifts by one year). Save images to
   `screenshots/`.
3. ⏳ **Paste earnings forecasts** into `inputs/forecasts_earnings.csv` (duplicate
   the templated ULTRACEMCO block for all 20), then run `py scripts/analyze.py`
   and copy the printed MAPE-by-cap and MAPE-by-horizon tables into Q2.
4. ⏳ **Q3 improved strategy.** Re-forecast all 20 with the fixed Q3 prompt, save to
   a second copy of the earnings file, re-score, and report the MAPE reduction.
5. ⏳ **Q4 earnings surprise.** Fill `inputs/earnings_announcements.csv` with each
   result `announce_date`, `actual_eps`, and your `forecast_eps`; run
   `analyze.py` for the surprise and the positive/negative-basket returns;
   compare to NIFTY over the same windows. (Prices 2021–2025 are already loaded.)
6. ⏳ **Q6 price forecasts.** Give the LLM the 2024 series from `data/prices_2024.csv`
   with the Q6 prompt; paste the three predictions per ticker into
   `inputs/forecasts_prices.csv`; run `analyze.py` for the directional hit-rate
   and abs-% error.
7. ⏳ **Fill the FY22 actuals + base figures.** The free price/financials source
   only exposed FY23–FY25, so the **FY22 column** in the actuals tables below is
   blank (shown as "—"). Read FY2022 *and* the FY2021 prompting base
   (revenue / net income) for each name from the consolidated *Statement of
   Profit and Loss* in `reports/<COMPANY>_FY2022.pdf` and type them in. Also
   verify the ⚠ HSIL numbers against `reports/HSIL_FY2022.pdf` (HSIL is now
   AGI Greenpac, BSE 500187).
8. ⏳ **Write the narrative** for Q2(a/b), Q5 and Q6 using the bullet skeletons in
   this report plus your scored numbers.

---

## How to run the exercise

1. **Get the source reports.** All annual-report PDFs are already downloaded to the
   `reports/` folder as `<COMPANY>_FY2021.pdf` / `<COMPANY>_FY2022.pdf` (38 files).
   Direct BSE links are in `data/annual_report_links.md` / `.csv`; re-run
   `py scripts/download_reports.py` to refresh. **Note:** ACC and AMBUJACEM have no
   FY2022 (Mar-2022) report — both were Jan–Dec calendar-year filers that moved to
   a March year-end via a 15-month transition report (Jan-2022→Mar-2023, filed as
   "FY2023"). Their FY2021 file = calendar year 2021. So 38/40 is the complete
   obtainable set.
2. **Forecast (Q1.1).** In a *fresh* chat, attach one report and paste the
   baseline prompt from `prompts/llm_prompts.md`. Save the screenshot. The prompt
   forces the model to forecast from the attached statements, not from memory.
3. **Record predictions** in `inputs/forecasts_earnings.csv` (rows are already
   templated for ULTRACEMCO — duplicate the block for all 20 companies).
4. **Score.** Run `py scripts/analyze.py`. It computes
   `Percentage Difference = (Actual − Predicted) / Actual × 100`
   against the downloaded actuals and aggregates MAPE by cap bucket and horizon.
5. Repeat with the **improved prompt (Q3)** in a separate column/file and compare.

---

## Q1.1 — Forecasts vs actuals

The LLM produces the **predicted** values; the **actual** values are downloaded
and shown below (Rs crore, consolidated, fiscal year ending 31 March). Empty
cells = the free data source did not expose that year; read those from the PDF.

### Actual Revenue (Rs crore)

| Bucket | Company | FY22 | FY23 | FY24 | FY25 |
|---|---|--:|--:|--:|--:|
| Large | ACC | 17,419 | — | 19,574 | 20,830 |
| Large | AMBUJACEM | 30,983 | — | 32,530 | 33,654 |
| Large | BIRLACORPN | — | 8,508 | 9,470 | 9,214 |
| Large | DALBHARAT | — | 13,237 | 14,334 | 13,980 |
| Large | GRASIM | — | 1,16,467 | 1,29,579 | 1,48,478 |
| Large | HEIDELBERG | — | 2,209 | 2,358 | 2,149 |
| Large | JKLAKSHMI | — | 6,451 | 6,788 | 6,193 |
| Large | RAMCOCEM | — | 8,122 | 9,349 | 8,518 |
| Large | SHREECEM | — | 17,441 | 20,092 | 19,283 |
| Large | ULTRACEMCO | — | 62,338 | 69,810 | 75,955 |
| Mid | JKCEMENT | — | 9,504 | 11,203 | 11,879 |
| Mid | ORIENTCEM | — | 2,934 | 3,177 | 2,704 |
| Mid | PRISMCEM | — | 7,210 | 7,331 | 6,780 |
| Mid | NCLIND | — | 1,610 | 1,643 | 1,362 |
| Mid | BURNPUR | — | 146 | 134 | 0 |
| Small | SOMANYCERA | — | 2,465 | 2,590 | 2,643 |
| Small | CERA | — | 1,800 | 1,866 | 1,915 |
| Small | HSIL ⚠ | — | 109 | 106 | 107 |
| Small | ASTRAL | — | 5,145 | 5,629 | 5,832 |
| Small | SUPREMEIND | — | 9,137 | 10,080 | 10,359 |

### Actual Net Income / PAT (Rs crore)

| Bucket | Company | FY22 | FY23 | FY24 | FY25 |
|---|---|--:|--:|--:|--:|
| Large | ACC | 649 | — | 2,335 | 2,402 |
| Large | AMBUJACEM | 1,938 | — | 3,573 | 4,303 |
| Large | BIRLACORPN | — | 40 | 421 | 295 |
| Large | DALBHARAT | — | 1,035 | 826 | 683 |
| Large | GRASIM | — | 6,827 | 5,624 | 3,706 |
| Large | HEIDELBERG | — | 99 | 168 | 107 |
| Large | JKLAKSHMI | — | 359 | 488 | 277 |
| Large | RAMCOCEM | — | 315 | 360 | 273 |
| Large | SHREECEM | — | 1,271 | 2,396 | 1,123 |
| Large | ULTRACEMCO | — | 5,064 | 7,005 | 6,039 |
| Mid | JKCEMENT | — | 424 | 791 | 861 |
| Mid | ORIENTCEM | — | 123 | 175 | 91 |
| Mid | PRISMCEM | — | −103 | 181 | 80 |
| Mid | NCLIND | — | 44 | 93 | 25 |
| Mid | BURNPUR | — | −71 | −99 | −42 |
| Small | SOMANYCERA | — | 71 | 97 | 60 |
| Small | CERA | — | 209 | 239 | 246 |
| Small | HSIL ⚠ | — | 8 | 10 | 8 |
| Small | ASTRAL | — | 457 | 546 | 524 |
| Small | SUPREMEIND | — | 865 | 1,070 | 961 |

⚠ **HSIL** values from the free source look inconsistent with the post-demerger
entity; verify against the PDF/BSE before using.

For each company, `analyze.py` writes the per-row table with predicted, actual
and percentage difference to `inputs/earnings_scored.csv`.

---

## Q1.2 — Accuracy commentary (fill after scoring)

`analyze.py` prints two tables you copy here: **MAPE by cap bucket** and **MAPE
by horizon**, plus the cap × horizon cross-tab.

**(a) Large vs mid vs small cap.** Expected and to be confirmed by your numbers:
large-caps forecast most accurately. They have stable, diversified revenue,
analyst-grade disclosure, and the model has seen many similar large-cap
statements, so growth/margin extrapolation is well anchored. Small-caps are the
least accurate — earnings are small in absolute terms, so a modest rupee miss is
a large percentage miss, and one-off items (e.g. BURNPUR losses, HSIL
restructuring) swamp the trend.

**(b) Horizon.** Accuracy decays monotonically with horizon: Year 1 (FY+1) is
most accurate; Year 3 (FY+3) the least. Errors compound because each year is
built on the previous year's already-estimated base, and the model cannot
anticipate cyclical turns (cement demand, fuel/pet-coke cost swings) two to three
years out. Net income degrades faster than revenue because margin is a second
source of error layered on top of the revenue error.

---

## Q2 — (covered above) the two dimensions

Report the actual MAPE figures from `inputs/earnings_scored.csv`:

| MAPE (%) | Year 1 | Year 2 | Year 3 |
|---|--:|--:|--:|
| Large | _fill_ | _fill_ | _fill_ |
| Mid | _fill_ | _fill_ | _fill_ |
| Small | _fill_ | _fill_ | _fill_ |

Comment on (a) the row pattern (small > mid > large error) and (b) the column
pattern (error rising left→right). Net income is consistently harder than
revenue — show the same table for each metric.

---

## Q3 — Improved strategy (same for all companies & periods)

**Chosen strategy:** supply the model with the **trailing 3–4 year history** that
already sits in the report's comparative columns and force an **explicit
decomposition**: (1) compute revenue CAGR from history, (2) grow revenue at that
CAGR adjusted by MD&A demand commentary, (3) revert the net margin to its 3-year
average, (4) net income = revenue × margin. The exact, fixed wording is in
`prompts/llm_prompts.md` (Q3 block) and is applied identically across all 20
companies and both base years — satisfying the "same strategy throughout"
requirement.

**Why it helps:** the baseline prompt lets the model pick an implicit growth rate
and margin; anchoring it to a computed CAGR and an average margin removes
free-floating optimism, narrows the variance of forecasts, and most strongly
improves small-cap and longer-horizon cases where the unconstrained model tends
to over-extrapolate. Record the improved predictions in a second forecasts file
and re-run `analyze.py`; expect the largest MAPE reduction at Year 2–3 and for
small-caps.

---

## Q4 — Earnings-surprise signal and trading test

**Signal:**
`Earnings Surprise = (Actual EPS − Forecast EPS) / Price 5 trading days before announcement.`

**Trading rule:** if surprise > 0, buy at the **open of day +1** after the
results date and hold to **day +5**; compute the **buy-and-hold return**
`(P_sell / P_buy − 1)`. `analyze.py` now does this end-to-end: fill
`inputs/earnings_announcements.csv` with `company, announce_date, actual_eps,
forecast_eps` and it auto-pulls the close 5 days prior from
`data/prices_daily.csv` (2021–2025), computes the surprise, the day +1→+5
return, and the average return of the positive- vs negative-surprise baskets.
A sanity check already returns ~+0.78% for ULTRACEMCO around 25-Apr-2024.

**Procedure:** for each company and each results announcement (FY22–FY24), look
up the actual EPS and the announcement date, take the close 5 days prior from
`data/prices_2024_2025.csv` (extend the price download for earlier dates if
needed), compute the surprise, then the day +1→+5 return. Average the returns of
the **positive-surprise** basket and compare to the average return of the broad
market (NIFTY/NIFTY Midcap over the same windows).

**Interpretation to write up:** a "good" signal earns positive **abnormal**
(above-market) returns on the positive-surprise basket and negative on the
negative-surprise basket. Because these surprises are computed against an
*LLM* forecast (not a consensus analyst estimate), expect the signal to be
**noisy and weak** — the post-earnings-announcement-drift literature relies on
consensus estimates, and an LLM forecast is a far coarser benchmark.

---

## Q5 — Overall observation on LLM behaviour

Points to make, supported by your tables:

- LLMs are competent at **short-horizon, large-cap interpolation** but weak at
  **long-horizon, small-cap, cyclical** forecasting.
- They **regress toward smooth trends** — they extrapolate recent growth and
  stable margins and systematically miss inflection points and one-off items.
- Output is **sensitive to prompt structure**: the Q3 decomposition prompt
  materially changes the answer, which means the model is doing pattern-matching,
  not genuine financial reasoning.
- Without the guardrail prompt they can **leak memorised actuals**; the prompts
  are written to suppress this, but it must be checked.

**Verdict:** in their present form LLMs are a useful **assistant** — fast first-
pass models, scenario framing, statement parsing — but **not a substitute** for
an analyst. They lack access to forward order books, management guidance nuance,
and judgement on non-recurring items, and they cannot be held accountable for a
call. Best used as a productivity layer under analyst supervision.

---

## Q6 — Stock-price forecasting from 2024 daily data

Data downloaded: daily closes 01-Jan-2024 → 31-Dec-2025 in
`data/prices_daily.csv` (full history 2021–2025; 2024-only slice in
`prices_2024.csv`). The LLM is given **only the 2024 series** and asked for the
close on 31-Jan-2025, 31-Mar-2025 and 31-Dec-2025 (prompt in
`prompts/llm_prompts.md`, Q6).

**Actual closes (Rs)** used to score the forecasts (`data/price_targets.csv`):

| Company | 31-Dec-24 (base) | 31-Jan-25 | 31-Mar-25 | 31-Dec-25 |
|---|--:|--:|--:|--:|
| ULTRACEMCO | 11,426 | 11,487 | 11,510 | 11,784 |
| SHREECEM | 25,694 | 27,796 | 30,503 | 26,575 |
| GRASIM | 2,443 | 2,509 | 2,611 | 2,829 |
| AMBUJACEM | 536 | 513 | 538 | 556 |
| ACC | 2,053 | 2,008 | 1,943 | 1,738 |
| DALBHARAT | 1,767 | 1,866 | 1,822 | 2,131 |
| RAMCOCEM | 966 | 918 | 897 | 1,057 |
| JKLAKSHMI | 836 | 804 | 774 | 778 |
| BIRLACORPN | 1,238 | 1,168 | 1,056 | 1,064 |
| HEIDELBERG | 208 | 218 | 198 | 175 |
| JKCEMENT | 4,595 | 4,835 | 4,933 | 5,531 |
| ORIENTCEM | 343 | 341 | 340 | 171* |
| PRISMCEM | 170 | 141 | 135 | 136 |
| NCLIND | 219 | 203 | 182 | 201 |
| BURNPUR | 34 | 33 | 33 | 33 |
| SOMANYCERA | 639 | 510 | 420 | 400 |
| CERA | 7,587 | 6,688 | 5,639 | 5,236 |
| HSIL | 126 | 128 | 100 | 291 |
| ASTRAL | 1,652 | 1,507 | 1,294 | 1,389 |
| SUPREMEIND | 4,701 | 3,969 | 3,426 | 3,354 |

\* ORIENTCEM Dec-25 reflects a corporate action / adjusted price — verify.

**Scoring (run `analyze.py` after pasting forecasts into
`inputs/forecasts_prices.csv`):** for each target it reports
(a) **directional hit-rate** (did the model get up/down vs 31-Dec-2024 right?) and
(b) **mean absolute % error**.

**Expected inferences:**
- Direction is roughly a **coin-flip**, especially at the 1-month horizon — short-
  term equity moves are close to a random walk and not recoverable from a single
  year of past prices.
- Absolute error **grows with horizon** but, unlike earnings, even the near-term
  price call is unreliable because day-to-day prices carry little forecastable
  signal.
- The model tends to project the **2024 drift forward**, so it does best on names
  that simply trended (e.g. JKCEMENT, ULTRACEMCO up) and worst on names that
  **reversed** (e.g. CERA, SUPREMEIND, ASTRAL fell in 2025 after rising).
- **Conclusion:** LLMs cannot meaningfully forecast individual stock prices from
  price history alone — consistent with weak-form market efficiency. This is a
  sharper negative result than the earnings exercise, where fundamentals at least
  give the model something real to anchor on.

---

## Repository map

| Path | Purpose |
|---|---|
| `scripts/download_financials.py` | Annual revenue & net income for all 20 names |
| `scripts/download_prices.py` | 2021–2025 daily closes + price targets |
| `scripts/download_reports.py` | Downloads all annual-report PDFs into `reports/` |
| `scripts/analyze.py` | Percentage-difference scoring, MAPE tables, Q4 surprise + buy-and-hold |
| `prompts/llm_prompts.md` | Fixed prompts for Q1, Q3, Q4, Q6 |
| `inputs/forecasts_earnings.csv` | Paste LLM earnings forecasts here |
| `inputs/forecasts_prices.csv` | Paste LLM price forecasts here |
| `inputs/earnings_announcements.csv` | Paste result dates + actual/forecast EPS for Q4 |
| `data/` | Downloaded actuals (CSV + Excel) |
| `reports/` | 38 downloaded annual-report PDFs (FY2021 & FY2022) |
| `data/annual_report_links.md` / `.csv` | Direct BSE links to FY2021/FY2022 reports |
