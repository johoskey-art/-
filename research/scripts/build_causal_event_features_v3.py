#!/usr/bin/env python3
"""Rebuild causal, chronological breakout features from pinned daily close CSV.

Run from repo root: python research/scripts/build_causal_event_features_v3.py
Stores research/results/causal_event_features_v3.csv, exactly 93 events in v3.
All feature/signal selection uses dates <= t; future 20/60/120 windows ONLY
provide ex post outcome labels and dataset edge eligibility.
Known-leader universe (10 firms) and time split bias still exist.
"""
from __future__ import annotations
import csv, math
from pathlib import Path
from split_cycles_v1 import CASES as KR, SOURCE_COMMIT, SOURCE_REPO
from us_holdout_anchor_v1 import US_CASES, fetch_source, source_rows

WINDOWS = {
    "005380":("2006-01-01","2017-12-31"),
    "000270":("2006-01-01","2017-12-31"),
    "051910":("2006-01-01","2017-12-31"),
    "005490":("2001-01-01","2013-12-31"),
    "010140":("2001-01-01","2013-12-31"),
    "005930":("2008-01-01","2017-12-31"),
    "000660":("2010-01-01","2021-04-15"),
    "128940":("2011-01-01","2021-04-15"),
    "TSLA":("2015-01-01","2025-12-31"),
    "NVDA":("2010-01-01","2025-12-31"),
}
COLS = [
    "name","ticker","date","anchor","entry","ret21","ret63","accel",
    "phase","outcome_last_date","y20","y60","y120","split","sha",
]

def cfgs():
    kr=[dict(name=name,ticker=ticker,repo=SOURCE_REPO,commit=SOURCE_COMMIT,
             path=f"Korea_Stocks_Full/{ticker}.csv",sha=sha)
        for name,ticker,_,_,sha in KR]
    return kr+US_CASES

def scan(c):
    start,end=WINDOWS[c["ticker"]]
    prices=[p for p in source_rows(fetch_source(c))
            if start<=p["date"]<=end and p["close"]>0]
    last_signal=-1000
    output=[]
    for i in range(252,len(prices)-120):
        if i-last_signal<120:
            continue
        anchor=max(p["close"] for p in prices[i-252:i])
        entry=prices[i]["close"]
        if entry<=anchor:
            continue
        # CAUSAL screen: only past 252 + signal close; never filter on future!
        causal_prices=prices[i-252:i+1]
        if any(not (0.5 <= causal_prices[j]["close"]/causal_prices[j-1]["close"] <= 1.5)
               for j in range(1,len(causal_prices))):
            continue
        ret21=math.log(entry/prices[i-21]["close"])
        ret63=math.log(entry/prices[i-63]["close"])
        accel=ret21/21-ret63/63
        phase=("accelerating" if accel>.001
               else "decelerating" if accel<-.001 else "steady")
        outcomes={}
        for h in (20,60,120):
            later=prices[i+1:i+h+1]
            actual=max([entry]+[p["close"] for p in later])
            outcomes[f"y{h}"]=f"{math.log(actual/anchor):.9f}"
        last_day=prices[i+120]["date"]
        split=("train" if last_day<"2018-01-01"
               else "test" if prices[i]["date"]>="2018-01-01" else "purge")
        output.append(dict(
            name=c["name"],ticker=c["ticker"],date=prices[i]["date"],
            anchor=f"{anchor:.9f}",entry=f"{entry:.9f}",
            ret21=f"{ret21:.9f}",ret63=f"{ret63:.9f}",
            accel=f"{accel:.9f}",phase=phase,
            outcome_last_date=last_day,**outcomes,split=split,sha=c["sha"],
        ))
        last_signal=i
    return output

def main():
    rows=[]
    for cfg in cfgs():
        one=scan(cfg)
        print(cfg["ticker"],len(one))
        rows.extend(one)
    assert len(rows)==93,len(rows)
    counts={s:sum(r["split"]==s for r in rows)
            for s in ("train","purge","test")}
    assert counts=={"train":71,"purge":3,"test":19},counts
    output=Path("research/results/causal_event_features_v3.csv")
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLS);w.writeheader();w.writerows(rows)
    print("WROTE",output,"n",len(rows),"partitions",counts)

if __name__=="__main__":
    main()
