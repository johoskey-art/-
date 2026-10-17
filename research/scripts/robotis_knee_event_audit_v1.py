#!/usr/bin/env python3
"""Audit 108490 2025-05-14 with point-in-time, same-price-basis OHLCV.

Needs a complete 2024-2025 raw/consistently adjusted daily CSV supplied by
an auditable source. Incomplete windows produce NA; never infer 252-day
breakouts from 52-week headlines or monthly bars.

Usage:
 python research/scripts/robotis_knee_event_audit_v1.py --input /path/to/108490_2024_2025.csv
CSV required headers: date,open,high,low,close,volume (YYYY-MM-DD).
All OHLC fields MUST be in the same raw/adjusted unit.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

LOOKBACKS = (20, 60, 120, 240, 250, 252)

def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        needed = {"date", "open", "high", "low", "close", "volume"}
        if not needed.issubset(set(reader.fieldnames or ())):
            raise ValueError(f"missing columns: {needed - set(reader.fieldnames or ())}")
        rows = []
        for row in reader:
            bar = {"date": row["date"]}
            try:
                for k in needed - {"date"}:
                    bar[k] = float(row[k].replace(",", ""))
            except (ValueError, TypeError, AttributeError):
                continue
            if bar["close"] <= 0 or bar["volume"] <= 0:
                continue  # discard zero-volume pseudo-sessions
            if not (bar["low"] <= bar["open"] <= bar["high"] and
                    bar["low"] <= bar["close"] <= bar["high"]):
                raise ValueError(f"OHLC inconsistent (adjustment mixing?): {bar['date']}")
            rows.append(bar)
    rows.sort(key=lambda r: r["date"])
    days = [r["date"] for r in rows]
    if len(set(days)) != len(days):
        raise ValueError("duplicate valid trading dates")
    return rows

def audit(rows, date="2025-05-14"):
    matches = [i for i, r in enumerate(rows) if r["date"] == date]
    if not matches:
        raise ValueError(f"not in source: {date}")
    i = matches[0]
    day = rows[i]
    result = {
        "date": date, "prior_valid_sessions": i,
        "open": day["open"], "high": day["high"], "low": day["low"],
        "close": day["close"], "volume": day["volume"],
        "daily_pct": round(100*(day["close"]/rows[i-1]["close"]-1), 8) if i else None,
        "volume_ratio20": round(day["volume"]/(sum(x["volume"] for x in rows[i-20:i])/20), 8) if i >=20 else None,
    }
    for n in LOOKBACKS:
        if i < n:
            result[f"prior_{n}_max_close"] = None
            result[f"prior_{n}_max_high"] = None
            result[f"break_{n}_close"] = None
            result[f"break_{n}_high"] = None
        else:
            prev = rows[i-n:i]  # strictly BEFORE event
            mc = max(x["close"] for x in prev)
            mh = max(x["high"] for x in prev)
            result[f"prior_{n}_max_close"] = mc
            result[f"prior_{n}_max_high"] = mh
            result[f"break_{n}_close"] = int(day["close"] > mc)
            result[f"break_{n}_high"] = int(day["high"] > mh)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--target", default="2025-05-14")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    out = audit(load(args.input), args.target)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(out))
            writer.writeheader()
            writer.writerow(out)
    for k, v in out.items():
        print(f"{k}={v if v is not None else 'NA'}")

if __name__ == "__main__":
    main()
