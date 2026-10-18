#!/usr/bin/env python3
"""Reproduce conservative evidence for the blogger's 457190 2025-12-08 knee label.

Input is 33 observed daily *closes* from a secondary backtest table
(2025-10-24 through 2025-12-09). This is NOT full 252-day OHLCV.
Any 60/120/252-day non-breakout result is a witness proof: a higher
historical close on 2025-10-24 within the past 31 trading sessions.
We DO NOT estimate unavailable prior 60/120/252-day maxima or any highs
or trading-volume averages.
"""
import argparse
import csv
from pathlib import Path

EVENT = "2025-12-08"
TICKER = "457190"

def calculate(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows = sorted(({"date": r["date"], "close": int(r["close_krw"]),
                    "ticker": r["ticker"]} for r in rows), key=lambda r:r["date"])
    if len(set(r["date"] for r in rows)) != len(rows):
        raise ValueError("duplicate dates")
    if any(r["ticker"] != TICKER or r["close"] <= 0 for r in rows):
        raise ValueError("wrong ticker or prices")
    ids = [i for i, r in enumerate(rows) if r["date"] == EVENT]
    if len(ids) != 1:
        raise ValueError("event absent")
    i = ids[0]
    before = rows[:i]
    if len(before) != 31:
        raise ValueError("expected 31 consecutive saved prior trading sessions")
    if before[0]["date"] != "2025-10-24" or before[-1]["date"] != "2025-12-05":
        raise ValueError("window endpoints do not match source")
    today = rows[i]["close"]
    result = {"event": EVENT, "close": today,
              "daily_return_pct": 100*(today / before[-1]["close"]-1)}
    for n in (20, 29, 30, 31):
        prior = before[-n:]
        maxrow = max(prior, key=lambda r:r["close"])
        result[f"prior{n}max_close"] = maxrow["close"]
        result[f"prior{n}max_date"] = maxrow["date"]
        result[f"break_prior{n}close"] = today > maxrow["close"]
    # All n>=31 lookbacks contain 2025-10-24 with close 59,700 > today 59,500.
    # Price basis and chronological completeness of 31 saved sessions checked above.
    for n in (60, 120, 252):
        result[f"break_prior{n}close"] = False
        result[f"prior{n}max_close"] = None
        result[f"prior{n}known_witness"] = "2025-10-24:59700"
    assert result["break_prior20close"] is True
    assert result["break_prior29close"] is True
    assert result["break_prior30close"] is False
    assert result["break_prior31close"] is False
    assert all(result[f"break_prior{n}close"] is False for n in (60, 120, 252))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path,
                        default=Path("research/results/isu_457190_knee_20251208_close_window_v1.csv"))
    args = parser.parse_args()
    import json
    print(json.dumps(calculate(args.input), ensure_ascii=False, indent=2))
