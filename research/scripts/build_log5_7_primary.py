#!/usr/bin/env python3
"""Rebuild/verify the CURRENT LOG-primary 5/7 research stage means.

Price basis: historic Adj_Close adjusted-close cohort, 38 PROVISIONAL cycles.
Not a prediction engine, not the original Naver blogger's Fibonacci formula.

Usage (repository root):
  python research/scripts/build_log5_7_primary.py
  python research/scripts/build_log5_7_primary.py --write
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results" / "kr38_adjclose_log5_7_combined_20261020.csv"
DEST = ROOT / "log_primary" / "LOG_STAGE_MEANS_38_AND_QC37_20261020.csv"
COLS = [
    "population", "division_k", "stage_j", "relative_log_fraction",
    "mean_price_over_low", "median_price_over_low",
    "mean_adjacent_step_ratio", "episodes", "unique_companies",
    "price_basis", "method",
]
LABEL_ALL = "MAIN_38_PROVISIONAL"
LABEL_QC = "QC37_NO_HYOSUNG_2007"


def fixed(value: float) -> str:
    return f"{value:.9f}"


def get_samples(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 38:
        raise ValueError(f"Expected 38 rows, got {len(rows)}")
    if len({(x["cohort_year"], x["ticker"]) for x in rows}) != 38:
        raise ValueError("Duplicate cycle key in canonical input")
    if len({x["ticker"] for x in rows}) != 34:
        raise ValueError("Expected 34 unique companies")
    parsed = []
    for r in rows:
        low = float(r["adjusted_low_close"])
        high = float(r["adjusted_peak_close"])
        reported = float(r["R_total"])
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low < high):
            raise ValueError(f"Invalid adjusted-close L/H: {r}")
        ratio = high / low
        if not math.isclose(reported, ratio, rel_tol=1e-8):
            raise ValueError(f"Stored R disagrees with adjusted-close L/H: {r}")
        for k, fld in [(5, "step5_log"), (7, "step7_log")]:
            if not math.isclose(float(r[fld]), ratio ** (1/k), rel_tol=1e-8):
                raise ValueError(f"Stored step factor wrong for {r['ticker']} at k={k}")
        qc = int(r["over_exchange_day_limit_events"])
        if qc < 0:
            raise ValueError("Negative quality event count")
        if not r["price_quality_status"] in (
            "ORIGINAL_30_ADJCLOSE", "RECOVERED_8_PROVISIONAL"
        ):
            raise ValueError("Unknown price-quality status")
        parsed.append(dict(ratio=ratio, ticker=r["ticker"], year=r["cohort_year"],
                           quality=qc, status=r["price_quality_status"]))
    if sum(x["status"] == "RECOVERED_8_PROVISIONAL" for x in parsed) != 8:
        raise ValueError("Expected 8 provisional recoveries")
    qc_cases = [x for x in parsed if x["quality"] != 0]
    if len(qc_cases) != 1 or (qc_cases[0]["ticker"], qc_cases[0]["year"]) != ("004800", "2007"):
        raise ValueError("QC37 exclusion set changed: investigate before updating")
    return parsed


def compute(rows: list[dict]) -> list[dict[str, str]]:
    populations = [
        (LABEL_ALL, rows),
        (LABEL_QC, [r for r in rows if r["quality"] == 0]),
    ]
    result = []
    for label, cohort in populations:
        for k in (5, 7):
            step_factors = [r["ratio"] ** (1 / k) for r in cohort]
            for j in range(k + 1):
                levels = [r["ratio"] ** (j / k) for r in cohort]
                result.append({
                    "population": label,
                    "division_k": str(k),
                    "stage_j": str(j),
                    "relative_log_fraction": fixed(j / k),
                    "mean_price_over_low": fixed(statistics.mean(levels)),
                    "median_price_over_low": fixed(statistics.median(levels)),
                    "mean_adjacent_step_ratio": (
                        fixed(statistics.mean(step_factors)) if j > 0 else ""
                    ),
                    "episodes": str(len(cohort)),
                    "unique_companies": str(len({r["ticker"] for r in cohort})),
                    "price_basis": "Adj_Close",
                    "method": "GEOMETRIC_LOG_EQUAL_RATIO",
                })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true",
                        help="Replace the log stage means file only after the input QC checks")
    args = parser.parse_args()
    result = compute(get_samples(SOURCE))
    if args.write:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        with DEST.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=COLS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(result)
        print(f"WROTE {DEST}: {len(result)} stage-mean rows")
    else:
        with DEST.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            got = list(reader)
            if reader.fieldnames != COLS:
                raise AssertionError(f"Unexpected header in {DEST}")
        if got != result:
            mismatch = next((i for i, (a,b) in enumerate(zip(got, result)) if a != b), None)
            raise AssertionError(f"Outdated log summary (first mismatch row={mismatch}), run --write after review")
        print(f"PASS: {len(result)}/28 logarithmic stage means match {DEST}")
    for label, cohort in [
        (LABEL_ALL, get_samples(SOURCE)),
        (LABEL_QC, [r for r in get_samples(SOURCE) if r["quality"] == 0]),
    ]:
        s5 = statistics.mean(r["ratio"] ** (1 / 5) for r in cohort)
        s7 = statistics.mean(r["ratio"] ** (1 / 7) for r in cohort)
        print(f"{label}: n={len(cohort)}, log5={s5:.9f}, log7={s7:.9f}")


if __name__ == "__main__":
    main()
