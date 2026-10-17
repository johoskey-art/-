#!/usr/bin/env python3
"""Anchor at each 52-week breakout: PRE-SIGNAL confirmed swing pivot vs prior-252d high.
Run from repository root: python research/scripts/breakout_swing_anchors_v1.py

Input events are from breakout_controls_v1.csv, which was preselected using
a future-adjacent jump integrity screen. Source CSVs are pinned by blob SHA.
The pivot algorithm uses ONLY closes strictly before each signal date.
"""
from __future__ import annotations
import csv
from pathlib import Path

from split_cycles_v1 import CASES as KR_CASES, SOURCE_COMMIT, SOURCE_REPO
from us_holdout_anchor_v1 import US_CASES, fetch_source, source_rows

INPUT = Path("research/results/breakout_controls_v1.csv")
OUTPUT = Path("research/results/breakout_swing_anchors_93_v1.csv")
COLUMNS = [
    "stock","ticker","date","entry","anchor252","pivot_date","pivot_price",
    "pivot_count","anchor_pivot_over_252","futuremax","reach1618_252",
    "reach1618_pivot","reach1272_252","reach1272_pivot","source_sha",
]
RATIOS = (1.272,1.618)

def configs():
    kr=[
        dict(name=n,ticker=t,repo=SOURCE_REPO,commit=SOURCE_COMMIT,
             path=f"Korea_Stocks_Full/{t}.csv",sha=sha)
        for n,t,_,_,sha in KR_CASES
    ]
    return kr+US_CASES

def latest_pivot(hist):
    pivots=[]
    for j in range(20,len(hist)-20):
        value=hist[j]["close"]
        if value < max(p["close"] for p in hist[j-20:j]):
            continue
        if value <= max(p["close"] for p in hist[j+1:j+21]):
            continue
        # Drawdown >=15% must have happened BEFORE breakout; no forward knowledge.
        if min(p["close"] for p in hist[j+1:]) > 0.85*value:
            continue
        pivots.append(hist[j])
    return (pivots[-1] if pivots else None,len(pivots))

def main():
    with INPUT.open(newline="",encoding="utf-8") as f:
        events=list(csv.DictReader(f))
    by_ticker={}
    for c in configs():
        by_ticker[c["ticker"]]=source_rows(fetch_source(c))
    results=[]
    for e in events:
        t=e["ticker"]
        a=by_ticker[t]
        by_date={p["date"]:i for i,p in enumerate(a)}
        i=by_date[e["date"]]
        hist=a[max(0,i-756):i]
        pivot,number=latest_pivot(hist)
        entry=float(e["entry"])
        anchor=float(e["prior52wkHigh"])
        futuremax=entry*(1+float(e["max120"]))
        pval=pivot["close"] if pivot else None
        row=dict(
            stock=e["name"],ticker=t,date=e["date"],
            entry=f"{entry:.8f}",anchor252=f"{anchor:.8f}",
            pivot_date=pivot["date"] if pivot else "",
            pivot_price=f"{pval:.8f}" if pivot else "",
            pivot_count=number,
            anchor_pivot_over_252=f"{pval/anchor:.8f}" if pivot else "",
            futuremax=f"{futuremax:.8f}",
            reach1618_252=str(futuremax>=1.618*anchor).lower(),
            reach1618_pivot=str(futuremax>=1.618*pval).lower() if pivot else "",
            reach1272_252=str(futuremax>=1.272*anchor).lower(),
            reach1272_pivot=str(futuremax>=1.272*pval).lower() if pivot else "",
            source_sha=e["source_sha"],
        )
        results.append(row)
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows(results)
    for key in ("reach1618_252","reach1618_pivot","reach1272_252","reach1272_pivot"):
        print(key,sum(x[key]=="true" for x in results),
              "/",sum(x[key] in ("true","false") for x in results))
    print("wrote",len(results),"events",OUTPUT)

if __name__=="__main__":
    main()
