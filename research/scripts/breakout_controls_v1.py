#!/usr/bin/env python3
"""Negative-control screen: unscreened 52-week CLOSE breakouts, fixed 120-day horizon.
Written 2026-10-17. Does NOT reconstruct blogger's Fibonacci/Elliott indicator.
Usage: python research/scripts/breakout_controls_v1.py
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

from split_cycles_v1 import CASES as KR, SOURCE_REPO, SOURCE_COMMIT
from us_holdout_anchor_v1 import US_CASES, fetch_source, source_rows

WINDOWS = {
    "005380": ("2006-01-01","2017-12-31"),
    "000270": ("2006-01-01","2017-12-31"),
    "051910": ("2006-01-01","2017-12-31"),
    "005490": ("2001-01-01","2013-12-31"),
    "010140": ("2001-01-01","2013-12-31"),
    "005930": ("2008-01-01","2017-12-31"), # stop before 2018 50-for-1 split
    "000660": ("2010-01-01","2021-04-15"),
    "128940": ("2011-01-01","2021-04-15"),
    "TSLA": ("2015-01-01","2025-12-31"),
    "NVDA": ("2010-01-01","2025-12-31"),
}
FIELDS = [
    "name","ticker","date","entry","prior52wkHigh","ret120","max120",
    "min120","meets40","ret120negative","source_sha",
]

def configs():
    kr = [
        dict(name=name,ticker=ticker,repo=SOURCE_REPO,commit=SOURCE_COMMIT,
             path=f"Korea_Stocks_Full/{ticker}.csv",sha=sha)
        for name,ticker,_start,_end,sha in KR
    ]
    return kr + US_CASES

def main():
    output = []
    for c in configs():
        ticker = c["ticker"]
        start, end = WINDOWS[ticker]
        raw = source_rows(fetch_source(c))
        rows = [r for r in raw if start<=r["date"]<=end]
        last = -1000
        rejected = 0
        for i in range(252,len(rows)-120):
            if i-last < 120:
                continue
            prevmax = max(p["close"] for p in rows[i-252:i])
            p = rows[i]
            if p["close"] <= prevmax:
                continue
            # Avoid mechanical split contamination and unadjusted discontinuities.
            segment = rows[i-252:i+121]
            if any(not 0.5 <= segment[j]["close"]/segment[j-1]["close"] <= 1.5
                   for j in range(1,len(segment))):
                rejected += 1
                continue
            future=rows[i+1:i+121]
            max120=max(x["close"] for x in future)/p["close"]-1
            min120=min(x["close"] for x in future)/p["close"]-1
            r120=rows[i+120]["close"]/p["close"]-1
            output.append({
                "name":c["name"],"ticker":ticker,"date":p["date"],
                "entry":f"{p['close']:.6f}",
                "prior52wkHigh":f"{prevmax:.6f}",
                "ret120":f"{r120:.6f}",
                "max120":f"{max120:.6f}",
                "min120":f"{min120:.6f}",
                "meets40":str(max120>=0.40).lower(),
                "ret120negative":str(r120<0).lower(),
                "source_sha":c["sha"],
            })
            last=i
        print(ticker,"signals",sum(z["ticker"]==ticker for z in output),"rejected",rejected)
    path=Path("research/results/breakout_controls_v1.csv")
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(output)
    print("Total eligible signals:",len(output))

if __name__=="__main__":
    main()
