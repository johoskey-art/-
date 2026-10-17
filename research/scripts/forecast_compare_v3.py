#!/usr/bin/env python3
"""Stage-aware price band v3 — reproduces 2026-10-17 pilot without web access.

Input: research/results/causal_event_features_v3.csv.
Output: research/results/forecast_comparison_v3.csv.
Precommitted choices:
- Train only records with last outcome date BEFORE 2018-01-01.
- Test record date ON/AFTER 2018-01-01; purge the boundary records.
- H=20,60,120 trading days. Future max includes today's close.
- Target y=log(max(Close[t],Close[t+1:t+h])/prev252_close_high).
- 80th conditional quantile, regime alpha=0.001 log/day, group shrink lambda=12.
- Momentum slope=0.2 * clip(alpha*h,-0.25,+0.25) (unfitted).
- Clamp predicted upper band to today's Close to avoid impossible target.
- Compare fixed multipliers 1.272, 1.618 and three predeclared models.
Usage: python research/scripts/forecast_compare_v3.py

The 93 event features were independently computed from pinned GitHub daily-close
CSV files, with breakout screening based on PRE-EVENT data only; the resulting
10-stock dataset still has survivorship bias and correlated stock observations.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path("research/results")
INPUT = ROOT / "causal_event_features_v3.csv"
OUTPUT = ROOT / "forecast_comparison_v3.csv"
Q = 0.80
LAMBDA = 12
REGIME_THRESHOLD = 0.001
MOM_COEFF = 0.20
HORIZONS = (20,60,120)
MODELS = ("fib1272","fib1618","hist80","regime80","momentum80")
COLUMNS = (
    "name","ticker","date","horizon","phase","accel","anchor","entry",
    "actual_future_logmax","model","predicted_logmax","predicted_target_price",
    "actual_future_max_price","pinball_loss","covered","sha"
)

def quantile(values, q):
    a = sorted(values)
    if not a:
        raise ValueError("No training values")
    x = (len(a)-1)*q
    i = math.floor(x)
    return a[i] + (a[min(i+1,len(a)-1)]-a[i])*(x-i)

def phase_for(acceleration):
    if acceleration > REGIME_THRESHOLD:
        return "accelerating"
    if acceleration < -REGIME_THRESHOLD:
        return "decelerating"
    return "steady"

def build():
    with INPUT.open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    train=[r for r in rows if r["outcome_last_date"]<"2018-01-01"]
    test=[r for r in rows if r["date"]>="2018-01-01"]
    assert len(train)==71 and len(test)==19, (len(train),len(test))
    assert all(phase_for(float(r["accel"])) == r["phase"] for r in rows)

    models_for_horizon = {}
    for h in HORIZONS:
        key=f"y{h}"
        global_q=quantile([float(r[key]) for r in train],Q)
        group={}
        for phase in ("accelerating","decelerating","steady"):
            subset=[float(r[key]) for r in train if r["phase"]==phase]
            weight=len(subset)/(len(subset)+LAMBDA)
            group[phase]=weight*quantile(subset,Q)+(1-weight)*global_q
        models_for_horizon[h]=(global_q,group)

    result=[]
    for r in test:
        entry=float(r["entry"])
        anchor=float(r["anchor"])
        acceleration=float(r["accel"])
        lower=math.log(entry/anchor)
        for h in HORIZONS:
            y=float(r[f"y{h}"])
            global_q,group=models_for_horizon[h]
            p={
                "fib1272":math.log(1.272),
                "fib1618":math.log(1.618),
                "hist80":global_q,
                "regime80":group[r["phase"]],
                "momentum80":global_q+MOM_COEFF*max(-0.25,min(0.25,acceleration*h)),
            }
            for model in MODELS:
                predicted=max(lower,p[model])
                score=Q*(y-predicted) if y>=predicted else (1-Q)*(predicted-y)
                result.append(dict(
                    name=r["name"],ticker=r["ticker"],date=r["date"],
                    horizon=h,phase=r["phase"],accel=f"{acceleration:.9f}",
                    anchor=f"{anchor:.9f}",entry=f"{entry:.9f}",
                    actual_future_logmax=f"{y:.9f}",model=model,
                    predicted_logmax=f"{predicted:.9f}",
                    predicted_target_price=f"{anchor*math.exp(predicted):.9f}",
                    actual_future_max_price=f"{anchor*math.exp(y):.9f}",
                    pinball_loss=f"{score:.9f}",covered=str(y<=predicted).lower(),
                    sha=r["sha"],
                ))
    return result

def main():
    rows=build()
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    for h in HORIZONS:
        for model in MODELS:
            r=[z for z in rows if z["horizon"]==h and z["model"]==model]
            print(f"h={h} {model}: q-loss={sum(float(z['pinball_loss']) for z in r)/len(r):.5f}; upper-covered={sum(z['covered']=='true' for z in r)}/{len(r)}")
    print("WROTE",OUTPUT,len(rows),"forecast observations")

if __name__=="__main__":
    main()
