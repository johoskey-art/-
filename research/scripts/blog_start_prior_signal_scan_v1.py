#!/usr/bin/env python3
"""Exploratory matched preceding-signal audit for two blogger-marked starts.

Replicates research/results/blog_start_preceding_120day_simultaneous_signals_v1.csv.
The >=5% and >=2x rule was selected AFTER seeing the blogger dates. Hence
uniqueness/frequency is descriptive, not independent validation or author formula.
Uses pinned source URLs and the data cleaning in blog_start_crosscheck_v2.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from blog_start_crosscheck_v2 import get_text, hd_rows, sk_rows, HD_URL, SK_URL

FIELDS = [
    "symbol","date","close_basis","close","high","volume",
    "previous_120_max_close","previous_120_max_high",
    "close_break_120","high_break_120","daily_return_pct","volume_ratio20",
    "passes_posthoc_return5_vol2","within_120_trading_days_from_target",
    "days_before_blog_date",
]

def scan(rows, symbol, first_date, target_date):
    idx = next(i for i,r in enumerate(rows) if r["date"] == target_date)
    for i in range(120, idx + 1):
        r = rows[i]
        if not first_date <= r["date"] <= target_date:
            continue
        prior = rows[i - 120:i]
        mc = max(x["close"] for x in prior)
        mh = max(x["high"] for x in prior)
        if r["close"] <= mc or r["high"] <= mh:
            continue
        pct = 100 * (r["close"] / rows[i - 1]["close"] - 1)
        pr20 = rows[i - 20:i]
        vr = r["volume"] / (sum(x["volume"] for x in pr20) / 20)
        days = idx - i
        yield {
            "symbol": symbol, "date": r["date"],
            "close_basis": "archival_Adj_Close" if symbol == "009540" else "archival_Close",
            "close": int(r["close"]), "high": int(r["high"]),
            "volume": int(r["volume"]),
            "previous_120_max_close": int(mc), "previous_120_max_high": int(mh),
            "close_break_120": 1, "high_break_120": 1,
            "daily_return_pct": f"{pct:.6f}",
            "volume_ratio20": f"{vr:.6f}",
            "passes_posthoc_return5_vol2": int(pct >= 5 and vr >= 2),
            "within_120_trading_days_from_target": int(days <= 120),
            "days_before_blog_date": days,
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
        default=Path(__file__).resolve().parents[1] / "results" /
        "blog_start_preceding_120day_simultaneous_signals_v1.csv")
    args = parser.parse_args()
    hh = list(scan(hd_rows(get_text(HD_URL)), "009540", "2004-01-01", "2005-01-05"))
    ss = list(scan(sk_rows(get_text(SK_URL)), "000660", "2022-08-18", "2023-07-27"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(hh + ss)
    print("009540", len(hh), "000660", len(ss), "strict", sum(int(x["passes_posthoc_return5_vol2"]) for x in hh + ss))

if __name__ == "__main__":
    main()
