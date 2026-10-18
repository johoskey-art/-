#!/usr/bin/env python3
"""Verify two separately blogger-labeled KNEE_CROSS dates from archived closes.

Inputs pinned in research/results; this is a close-only audit, not a recreation
of proprietary blogger knee-band values. 'Prior 20' means STRICTLY previous
20 positive-volume exchange sessions, no weekends or holiday snapshots.
The Robotis archive's YAML dates are misleading (same-day close recorded
in morning-timestamped page). Treat them as retrospective market snapshots.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

CASES = [
 ("108490", "2025-05-14", "research/results/robotis_108490_knee_20250514_verified_prev20_closes_v1.csv"),
 ("457190", "2025-12-08", "research/results/isu_457190_knee_20251208_close_window_v1.csv"),
]

def read_closes(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    results = []
    for row in rows:
        d = row["date"]
        v = float(row["close_krw"])
        if v <= 0: raise ValueError("nonpositive close "+d)
        results.append({"date":d, "close":v})
    if len(set(x["date"] for x in results)) != len(results):
        raise ValueError("duplicate dates or copied holiday snapshots")
    if results != sorted(results,key=lambda x:x["date"]):
        raise ValueError("dates not sorted")
    return results

def signal(rows, symbol, event_date):
    dates = [x["date"] for x in rows]
    if event_date not in dates: raise ValueError("event date missing")
    i = dates.index(event_date)
    if i < 21: raise ValueError("needs 20 days before event and 20 before previous day")
    day = rows[i]["close"]
    yesterday = rows[i-1]["close"]
    prior = rows[i-20:i]
    old_prior = rows[i-21:i-1]
    prev20avg = sum(x["close"] for x in prior)/20
    prev20max = max(x["close"] for x in prior)
    old20avg = sum(x["close"] for x in old_prior)/20
    old20max = max(x["close"] for x in old_prior)
    # Conventional SMA20 on day t includes C[t], unlike our strict
    # prior-20 reference mean used for breakout lookbacks.
    sma20_t = sum(x["close"] for x in rows[i-19:i+1]) / 20
    sma20_prev = sum(x["close"] for x in rows[i-20:i]) / 20
    return {
      "symbol":symbol, "event":event_date, "event_close":day,
      "previous_close":yesterday,
      "day_return_pct":round((day/yesterday-1)*100,6),
      "prior20_max_close":prev20max, "prior20_mean_close":prev20avg,
      "event_breaks_prior20_max":day>prev20max,
      "event_close_above_prior20_mean":day>prev20avg,
      "previous_day_breaks_its_prior20_max":yesterday>old20max,
      "previous_day_above_its_prior20_mean":yesterday>old20avg,
      "previous_day_prior20_max_close":old20max,
      "previous_day_prior20_mean_close":old20avg,
      "sma20_including_event":sma20_t,
      "sma20_including_previous_day":sma20_prev,
      "crosses_conventional_sma20":day>sma20_t and yesterday<=sma20_prev,
      "event_is_first_20d_break_after_previous_day":day>prev20max and not(yesterday>old20max),
      "event_crosses_above_ma20_from_yesterday":
        (day>prev20avg) and (yesterday<=old20avg),
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",type=Path,default=Path("."))
    args=ap.parse_args()
    results=[signal(read_closes(args.repo_root/path), symbol, date)
             for symbol,date,path in CASES]
    bysym={x["symbol"]:x for x in results}
    assert bysym["108490"]["event_close"]==49000
    assert bysym["108490"]["prior20_max_close"]==37700
    assert bysym["108490"]["prior20_mean_close"]==35330
    assert bysym["108490"]["sma20_including_event"]==36090
    assert not bysym["108490"]["crosses_conventional_sma20"]
    assert bysym["108490"]["previous_day_breaks_its_prior20_max"]
    assert bysym["108490"]["previous_day_above_its_prior20_mean"]
    assert not bysym["108490"]["event_is_first_20d_break_after_previous_day"]
    assert bysym["457190"]["event_close"]==59500
    assert bysym["457190"]["prior20_max_close"]==55600
    assert bysym["457190"]["prior20_mean_close"]==51982.5
    assert bysym["457190"]["sma20_including_event"]==52227.5
    assert bysym["457190"]["crosses_conventional_sma20"]
    assert bysym["457190"]["event_is_first_20d_break_after_previous_day"]
    print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
