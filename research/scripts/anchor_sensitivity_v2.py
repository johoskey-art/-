#!/usr/bin/env python3
"""Experiment v2: sensitivity of previous-cycle anchor definitions.

Outputs 10 * 5 = 50 records (including ineligible anchors).
Run from repository root:
  python research/scripts/anchor_sensitivity_v2.py
Requires internet and original pinned source GitHub files.

ALL episodes are selected by their ex-post 2003-2024 bottoms and tops.
Anchor data is restricted to dates before each bottom. Do not interpret
the eventual peak/anchor ratios as prospective forecasts.
"""
from __future__ import annotations

import csv
import math
from datetime import date, timedelta
from pathlib import Path

from split_cycles_v1 import CASES as KR_CASES, SOURCE_COMMIT, SOURCE_REPO
from us_holdout_anchor_v1 import US_CASES, fetch_source, source_rows, episode

COLS = [
    "symbol", "ticker", "start_low_date", "start_low_close",
    "ex_post_peak_date", "ex_post_peak_close", "anchor_type",
    "anchor_date", "anchor_price", "anchor_to_low_ratio",
    "final_peak_to_anchor_ratio", "anchor_fraction_of_total_rise",
    "eligible_prior_observations", "source_repo", "source_blob_sha",
    "eligibility_note",
]

def cfgs():
    kr = [
        dict(name=name, ticker=ticker, start=search_start, end=search_end,
             repo=SOURCE_REPO, path=f"Korea_Stocks_Full/{ticker}.csv",
             commit=SOURCE_COMMIT, sha=sha)
        for name, ticker, search_start, search_end, sha in KR_CASES
    ]
    return kr + US_CASES

def trunc_yrs(d, yrs):
    days = math.floor(yrs * 365.25 + .5)
    return date.fromisoformat(d) - timedelta(days=days)

def record(c, low, peak, typ, a, count, status):
    low_val, high_val = low["close"], peak["close"]
    return {
        "symbol":c["name"], "ticker":c["ticker"],
        "start_low_date":low["date"],"start_low_close":f"{low_val:.8f}",
        "ex_post_peak_date":peak["date"],
        "ex_post_peak_close":f"{high_val:.8f}",
        "anchor_type":typ,
        "anchor_date":a["date"] if a else "",
        "anchor_price":f"{a['close']:.8f}" if a else "",
        "anchor_to_low_ratio":f"{a['close']/low_val:.8f}" if a else "",
        "final_peak_to_anchor_ratio":f"{high_val/a['close']:.8f}" if a else "",
        "anchor_fraction_of_total_rise":
            f"{(a['close']-low_val)/(high_val-low_val):.8f}" if a else "",
        "eligible_prior_observations":count,
        "source_repo":c["repo"],"source_blob_sha":c["sha"],
        "eligibility_note":status,
    }

def calculate(c):
    full = source_rows(fetch_source(c))
    low, peak, _, _ = episode(full,c)
    i0 = next(i for i,x in enumerate(full) if x["date"]==low["date"])
    before = full[:i0]
    output = []
    for yrs in (1,2,3,5):
        cutoff = trunc_yrs(low["date"],yrs)
        eligible = [x for x in before if date.fromisoformat(x["date"])>=cutoff]
        mincount=math.floor(yrs*252*.72+.5)
        a = max(eligible,key=lambda x:x["close"]) if len(eligible)>=mincount else None
        output.append(record(
            c,low,peak,f"rolling_max_{yrs}y",a,len(eligible),
            "ok" if a else "insufficient_history"))
    # Confirmed close swing high: last candidate within 3 calendar years
    # that dominates the PREVIOUS 20 and NEXT 20 trading-day closes.
    # 20-day confirmation must be complete by the ex-post cycle low.
    hist = [x for x in before
            if date.fromisoformat(x["date"])>=trunc_yrs(low["date"],3)]
    pivots=[]
    for i in range(20,len(hist)-20):
        x=hist[i]
        if (x["close"] >= max(z["close"] for z in hist[i-20:i])
            and x["close"] > max(z["close"] for z in hist[i+1:i+21])
            and x["close"]/low["close"]>=1.15):
            pivots.append(x)
    output.append(record(
        c,low,peak,"last_confirmed_pivot_20x20_15pct",
        pivots[-1] if pivots else None,len(pivots),
        "ok" if pivots else "no_pivot"))
    return output

def main():
    records=[]
    for c in cfgs():
        recs=calculate(c)
        records.extend(recs)
        print(c["ticker"],len(recs),
              [(r["anchor_type"],r["final_peak_to_anchor_ratio"])
               for r in recs])
    out=Path("research/results/anchor_sensitivity_10_v2.csv")
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=COLS)
        w.writeheader();w.writerows(records)
    print("Wrote",out,len(records),"rows")

if __name__=="__main__":
    main()
