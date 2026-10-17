#!/usr/bin/env python3
"""Generate fixed Fibonacci extension touch labels from existing breakout dataset.

Run from repository root:
  python research/scripts/fib_breakout_targets_v1.py

The input 93 events and their 120-day observed future max CLOSE were already
computed by breakout_controls_v1.py. This file merely compares those observations
to fixed multiples of the previous 252 trading-day CLOSE high.
"""
from __future__ import annotations
import csv
from pathlib import Path

INPUT = Path("research/results/breakout_controls_v1.csv")
OUTPUT = Path("research/results/fib_breakout_targets_93_v1.csv")
RATIOS = (1.272, 1.618, 2.0, 2.618)
FIELDS = (
    "name", "ticker", "signal_date", "entry_close", "prior252_high_close",
    "extension_ratio", "target_price", "observed_future_120_max_close",
    "touch_within_120d", "source_sha"
)

def main():
    with INPUT.open(encoding="utf-8", newline="") as f:
        events = list(csv.DictReader(f))
    records=[]
    for row in events:
        entry=float(row["entry"])
        anchor=float(row["prior52wkHigh"])
        max_future=entry*(1.0+float(row["max120"]))
        for ratio in RATIOS:
            target=anchor*ratio
            records.append(dict(
                name=row["name"], ticker=row["ticker"], signal_date=row["date"],
                entry_close=f"{entry:.8f}", prior252_high_close=f"{anchor:.8f}",
                extension_ratio=f"{ratio:.8f}", target_price=f"{target:.8f}",
                observed_future_120_max_close=f"{max_future:.8f}",
                touch_within_120d=str(max_future>=target).lower(),
                source_sha=row["source_sha"],
            ))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        w.writeheader()
        w.writerows(records)
    for ratio in RATIOS:
        touched=sum(1 for r in records
                    if float(r["extension_ratio"]) == ratio
                    and r["touch_within_120d"] == "true")
        print(f"r={ratio:.3f}: touched {touched}/{len(events)}")
    print("Wrote",OUTPUT,len(records),"rows")

if __name__=="__main__":
    main()
