# KR-only historical leader pilot: frozen candidates and cohort rules (2026-10-17)

**Target:** Prioritize Korean sector cycles and learn cross-stock stage multipliers from rising **price**, not rising time. No fitted Fibonacci coefficients.

## Candidate provenance
All 46 **candidate episodes** were transcribed from the **Korean 60 leader candidates** on p11 of `주도주사이클절대법칙v5_한규범_강의자료(HS아카데미 26.08.13).pdf`; repeated names in a different year remain distinct candidate *episodes*. This is a completely separate research author's presentation, NOT source of the target Naver blogger's exact Fibonacci code. Mapping names to current tickers and provisional broad sectors is analyst supplied, must be reverified for historic business reorganizations. The 2020 cohort will be **right-censored** in the 2021-04-ending archived source: flag it as censored and do not present as completed 2022-cycle.

## Frozen selection windows (prior to looking at resulting price multiples)
- Source: `choosunsick/Korea_Stocks` daily CSV; pin per-file blob SHA to each observation. Archive endpoint Apr 2021. No license-controlled PDF or chart images republished.
- For PDF year Y: seek minimum CLOSE among [Jan 1 Y-1, Dec 31 Y]; then highest CLOSE after the selected low up to [Dec 31 Y+2]. If price archive ends early, **censor** (2020 year) rather than claim the peak is completed. No claim this picks original blogger's cycle.
- Store all attempted candidates, missing/IPO/renamed sources, discontinuities/invalid OHLC, insufficient coverage, and results separately: **do not discard non-Fibonacci-looking episodes**. Require at least 60 trading dates between extrema. QC >50% one-day jump, observed close outside high-low by >2% (separately flagged); flagged cases excluded from clean primary summary.
- For each completed sample R=H/L, compute *geometric* 5 & 7 equal-multiplicative-step factors R^(1/5), R^(1/7), **also linear equal-price-step relative values** [1+(R-1)j/k], k∈{5,7}. Report individual observations, arithmetic mean, median, percentiles, unweighted stock vs episode, industry cohorts and uncertainty. Compare phi only **after** publishing the full distribution.
- Crucial: the mean of R^(1/5) does not imply that Fibonacci is the source formula; 5/7 measurements are algebraically related through the same R.
- Do not mix historic raw close with modern stock-split-adjusted values across periods. Price source metadata, timestamp, exclusions documented.

## Next
Fetch frozen candidates, generate QC ledger + clean episode dataset + grouped 5/7 statistics, then expand only with explicit new cohorts/source coverage. Full study path in `research/README.md`.
