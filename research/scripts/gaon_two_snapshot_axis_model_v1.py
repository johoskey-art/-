#!/usr/bin/env python3
"""Exploratory Gaon source-screen price axis audit; NOT band price estimates.

Compare two axes using raw tick centers manually read from screenshots.
Linear: y = a + b*price
Log: y = a + b*ln(price)
RMSE uses ONLY tick centers, does not establish author algorithm.
"""
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

def fit(xs,ys):
    mx=sum(xs)/len(xs);my=sum(ys)/len(ys)
    slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    base=my-slope*mx
    error=math.sqrt(sum((y-(base+slope*x))**2 for x,y in zip(xs,ys))/len(xs))
    return base,slope,error

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",type=Path,default=Path("research/results/gaon_20260511_20261014_axis_tick_calibration_v1.csv"))
    args=p.parse_args()
    series=defaultdict(list)
    with args.csv.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):
            series[r["snapshot_date"]].append((float(r["axis_price_krw"]),float(r["y_axis_tick_approx_px"])))
    assert set(series)=={"2026-05-11","2026-10-14"}
    for snapshot,rows in sorted(series.items()):
        price,pixel=zip(*rows)
        linear=fit(price,pixel)
        log=fit([math.log(p) for p in price],pixel)
        print(snapshot,"linear_RMSE_px=",round(linear[-1],4),
              "log_RMSE_px=",round(log[-1],4),
              "preferred_screen_axis=","linear" if linear[-1]<log[-1] else "log")
        if snapshot=="2026-05-11":assert linear[-1]<2 and log[-1]>10
        if snapshot=="2026-10-14":assert log[-1]<3 and linear[-1]>7
    print("Corporate action: 2026 bonus issue 0.8 shares per old share -> divide pre-bonus old-scale prices by 1.8 for comparable quote units.")
    print("No claim about same-day band values, original author's adjustment, or repainting.")

if __name__=="__main__":main()
