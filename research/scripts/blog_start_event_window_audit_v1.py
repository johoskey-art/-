#!/usr/bin/env python3
"""Audit candidate blog cycle-start dates within a fixed archived trading-day window.

Input is the existing 009540 24-row table from 2026-10-17. The candidate
filters are EXPLORATORY, not a reconstruction of the blog author's rule.
No future prices enter the same-day signals. This is not an out-of-sample test.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "results" / "009540_20050105_breakout_window_v1.csv"

def read_rows(path: Path) -> list[dict[str, float | str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        raw = list(csv.DictReader(f))
    if not raw:
        raise ValueError("No data rows")
    return [{key: (val if key == "date" else float(val)) for key, val in row.items()} for row in raw]

def audit(rows: list[dict[str, float | str]]) -> list[tuple[str, list[str]]]:
    def b120(row): return row["breaks_120_adj_close"] == 1
    def b250(row): return row["breaks_250_adj_close"] == 1
    def v(row, threshold): return row["volume_to_prior_20_mean"] >= threshold
    def gain(row, threshold): return row["change_pct_from_prev_adj_close"] >= threshold
    def near250(row): return row["adjusted_close"] / row["prior_250_max_adj_close"] >= 0.98
    cases = [
        ("120d breakout", lambda x: b120(x)),
        ("120d + volume>=1.5x", lambda x: b120(x) and v(x, 1.5)),
        ("120d + volume>=2x", lambda x: b120(x) and v(x, 2)),
        ("120d + daily gain>=5pct", lambda x: b120(x) and gain(x, 5)),
        ("120d + volume>=2x + gain>=5pct", lambda x: b120(x) and v(x, 2) and gain(x, 5)),
        ("120d + volume>=2x + within2pct of prior250d", lambda x: b120(x) and v(x, 2) and near250(x)),
        ("250d breakout", lambda x: b250(x)),
    ]
    return [(label, [str(row["date"]) for row in rows if predicate(row)]) for label, predicate in cases]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=DEFAULT)
    args = parser.parse_args()
    rows = read_rows(args.csv)
    print(f"Trading-day rows in archive window: {len(rows)}")
    for label, dates in audit(rows):
        print(f"{label}: {len(dates)} | {', '.join(dates) if dates else '-'}")

if __name__ == "__main__":
    main()
