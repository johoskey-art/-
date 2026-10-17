#!/usr/bin/env python3
"""Rolling 20d adaptive upper bands over 19 out-of-time breakout events.

Train q=.8 using only 71 120-day-completed episodes before 2018-01-01.
Reforecast next 20d at signal day offsets 0/20/40/60, with all inputs known
at each reforecast. Pivot and Elliott wave classification are NOT used.
Output 76 origins * 4 methods = 304 records.
Usage: python research/scripts/rolling_band_eval_v3.py
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from split_cycles_v1 import SOURCE_COMMIT, SOURCE_REPO
from us_holdout_anchor_v1 import US_CASES, fetch_source, source_rows
from forecast_compare_v3 import quantile

ROOT=Path("research/results")
INPUT=ROOT/"causal_event_features_v3.csv"
OUTPUT=ROOT/"rolling_bands_20day_v3.csv"
COLUMNS=[
    "name","ticker","signal_date","date","day_offset","phase","accel",
    "entry","anchor","actual20_price","upper_price","model","score",
    "covered","source_sha",
]

def cfg_for(ticker,sha):
    if ticker in ("000660","128940"):
        return dict(name=ticker,ticker=ticker,repo=SOURCE_REPO,
                    commit=SOURCE_COMMIT,
                    path=f"Korea_Stocks_Full/{ticker}.csv",sha=sha)
    for cfg in US_CASES:
        if cfg["ticker"]==ticker:
            assert cfg["sha"]==sha
            return cfg
    raise ValueError(ticker)

def quantiles(train):
    gq=quantile([float(r["y20"]) for r in train],.8)
    stages={}
    for name in ("accelerating","steady","decelerating"):
        q=[float(r["y20"]) for r in train if r["phase"]==name]
        weight=len(q)/(len(q)+12)
        stages[name]=weight*quantile(q,.8)+(1-weight)*gq
    return gq,stages

def compute():
    with INPUT.open(encoding="utf-8",newline="") as f:
        events=list(csv.DictReader(f))
    train=[r for r in events if r["outcome_last_date"]<"2018-01-01"]
    tests=[r for r in events if r["date"]>="2018-01-01"]
    assert len(train)==71 and len(tests)==19
    base,group=quantiles(train)
    configs={r["ticker"]:cfg_for(r["ticker"],r["sha"]) for r in tests}
    price_data={k:source_rows(fetch_source(v)) for k,v in configs.items()}
    index={k:{p["date"]:i for i,p in enumerate(v)} for k,v in price_data.items()}
    output=[]
    for event in tests:
        name,ticker=event["name"],event["ticker"]
        rows=price_data[ticker]
        i0=index[ticker][event["date"]]
        for offset in (0,20,40,60):
            i=i0+offset
            price=rows[i]["close"]
            anchor=max(p["close"] for p in rows[i-252:i])
            delta=(math.log(price/rows[i-21]["close"])/21
                  -math.log(price/rows[i-63]["close"])/63)
            phase=("accelerating" if delta>.001
                   else "decelerating" if delta<-.001 else "steady")
            actual=max([price]+[p["close"] for p in rows[i+1:i+21]])
            truth=math.log(actual/anchor)
            floor=math.log(price/anchor)
            candidates={
                "fib1272":math.log(1.272),
                "hist80":base,
                "regime80":group[phase],
                "momentum80":base+.2*max(-.25,min(.25,delta*20)),
            }
            for model,target in candidates.items():
                pred=max(floor,target)
                loss=.8*(truth-pred) if truth>=pred else .2*(pred-truth)
                output.append(dict(
                    name=name,ticker=ticker,signal_date=event["date"],
                    date=rows[i]["date"],day_offset=offset,phase=phase,
                    accel=f"{delta:.9f}",entry=f"{price:.9f}",
                    anchor=f"{anchor:.9f}",actual20_price=f"{actual:.9f}",
                    upper_price=f"{anchor*math.exp(pred):.9f}",model=model,
                    score=f"{loss:.9f}",covered=str(truth<=pred).lower(),
                    source_sha=event["sha"],
                ))
    return output

def main():
    rows=compute()
    assert len(rows)==304
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS)
        writer.writeheader();writer.writerows(rows)
    for model in ("fib1272","hist80","regime80","momentum80"):
        z=[r for r in rows if r["model"]==model]
        mean=sum(float(x["score"]) for x in z)/len(z)
        print(model,f"{mean:.5f}","covered",sum(x["covered"]=="true" for x in z),"/",len(z))
    print("WROTE",OUTPUT,len(rows))

if __name__=="__main__":
    main()
