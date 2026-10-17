#!/usr/bin/env python3
"""Domestic 30 historical leader episodes — stock-internal means, then cross-stock means.

Run from repository root:
    python research/scripts/kr_30_price_split_two_level_means_v2.py

Requires only Python 3 standard library and the committed, previously audited
research/results/kr_30_clean_episodes_v1.csv. No forward return predictions.
Outputs are exactly price-grid arithmetic consequences of each ex-post (L,H)
pair, NOT measured mid-cycle closes, and NOT the original blogger's formula.
"""
import csv
import math
import statistics
from pathlib import Path

ROOT = Path("research/results")
SOURCE = ROOT / "kr_30_clean_episodes_v1.csv"
STOCK = ROOT / "kr_30_per_stock_two_stage_averages_v2.csv"
POINTS = ROOT / "kr_30_all_price_grid_levels_v2.csv"
SENSITIVITY = ROOT / "kr_30_averaging_definition_sensitivity_v2.csv"

STOCK_FIELDS = [
    "cohort_year", "stock_name", "ticker", "sector", "low_date", "low_close",
    "peak_date", "peak_close", "total_gain_R",
    "linear5_mean_of_levels", "linear7_mean_of_levels",
    "log5_mean_of_levels", "log7_mean_of_levels",
    "linear5_mean_step_ratio", "linear7_mean_step_ratio",
    "log5_mean_step_ratio", "log7_mean_step_ratio",
    "geometric_midpoint", "source_blob_sha"
]
POINT_FIELDS = [
    "cohort_year", "stock_name", "ticker", "sector", "scheme", "parts",
    "step", "relative_fraction", "target_multiple_over_low",
    "target_price_source_unit", "step_multiple_over_prev", "source_blob_sha"
]
SENS_FIELDS = [
    "split_k", "price_grid", "within_stock_average_definition",
    "cross_stock_mean", "cross_stock_median", "observed_min", "observed_max",
    "episode_count", "explanation"
]
CONVENTIONS = [
    ("include_low_and_high", lambda k: range(0,k+1), "j=0..k price levels, inclusive"),
    ("interior_levels_only", lambda k: range(1,k), "j=1..k-1, exclude both endpoints"),
    ("upper_endpoint_per_interval", lambda k: range(1,k+1), "j=1..k, exclude low"),
    ("lower_endpoint_per_interval", lambda k: range(0,k), "j=0..k-1, exclude peak"),
    ("adjacent_price_ratios", lambda k: range(1,k+1), "price ratio Pj/P(j-1), across k intervals")
]

def fmt(value):
    if value is None:
        return ""
    if isinstance(value,float):
        return f"{value:.12f}"
    return str(value)

def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key:fmt(row.get(key,"")) for key in fields})

def main():
    with SOURCE.open(encoding="utf-8",newline="") as fh:
        source=list(csv.DictReader(fh))
    if len(source)!=30:
        raise ValueError("Expected exactly 30 frozen domestic episodes; did the source change?")
    details=[]
    points=[]
    for record in source:
        low=float(record["low_close"])
        high=float(record["peak_close"])
        R=high/low
        if low<=0 or high<=low or not math.isclose(R,float(record["R"]),rel_tol=1e-10):
            raise ValueError("Invalid or changed L/H: "+record["name"]+" "+record["y"])
        row=dict(
            cohort_year=record["y"],stock_name=record["name"],
            ticker=record["ticker"],sector=record["sector"],
            low_date=record["low"],low_close=low,
            peak_date=record["peak"],peak_close=high,
            total_gain_R=R,geometric_midpoint=math.sqrt(R),
            source_blob_sha=record["source_sha"]
        )
        for k in (5,7):
            for scheme in ("linear","log"):
                levels=[
                    1+(R-1)*j/k if scheme=="linear" else R**(j/k)
                    for j in range(k+1)
                ]
                step_ratios=[
                    levels[j]/levels[j-1] for j in range(1,k+1)
                ]
                row[f"{scheme}{k}_mean_of_levels"]=statistics.mean(levels)
                row[f"{scheme}{k}_mean_step_ratio"]=statistics.mean(step_ratios)
                for j,value in enumerate(levels):
                    points.append(dict(
                        cohort_year=record["y"],stock_name=record["name"],
                        ticker=record["ticker"],sector=record["sector"],
                        scheme=scheme,parts=k,step=j,relative_fraction=j/k,
                        target_multiple_over_low=value,
                        target_price_source_unit=low*value,
                        step_multiple_over_prev=(step_ratios[j-1] if j else ""),
                        source_blob_sha=record["source_sha"]
                    ))
        # These are deterministic algebraic checks, not evidence of Fibonacci.
        exact_mid=(1+R)/2
        assert math.isclose(row["linear5_mean_of_levels"],exact_mid,rel_tol=1e-12)
        assert math.isclose(row["linear7_mean_of_levels"],exact_mid,rel_tol=1e-12)
        assert math.isclose(row["log5_mean_step_ratio"],R**(1/5),rel_tol=1e-12)
        assert math.isclose(row["log7_mean_step_ratio"],R**(1/7),rel_tol=1e-12)
        details.append(row)
    assert len(points)==840 and len(details)==30

    sensitivities=[]
    for k in (5,7):
        for scheme in ("linear","log"):
            for definition,indices,note in CONVENTIONS:
                values=[]
                for stock in details:
                    R=stock["total_gain_R"]
                    def level(j):
                        return 1+(R-1)*j/k if scheme=="linear" else R**(j/k)
                    v=[(level(j)/level(j-1) if definition=="adjacent_price_ratios"
                        else level(j)) for j in indices(k)]
                    values.append(statistics.mean(v))
                sensitivities.append(dict(
                    split_k=k,price_grid=scheme,
                    within_stock_average_definition=definition,
                    cross_stock_mean=statistics.mean(values),
                    cross_stock_median=statistics.median(values),
                    observed_min=min(values),observed_max=max(values),
                    episode_count=len(values),explanation=note
                ))
    write_csv(STOCK,STOCK_FIELDS,details)
    write_csv(POINTS,POINT_FIELDS,points)
    write_csv(SENSITIVITY,SENS_FIELDS,sensitivities)
    print("30 complete episodes, 840 synthetic price grid points, 20 definitions.")
    for scheme in ("linear","log"):
        for k in (5,7):
            print(scheme,k,"within-stock mean then cross-stock mean:",
                  f"{statistics.mean(r[f'{scheme}{k}_mean_of_levels'] for r in details):.6f}",
                  "adjacent step mean:",
                  f"{statistics.mean(r[f'{scheme}{k}_mean_step_ratio'] for r in details):.6f}")
    print("Stored stock / stage / sensitivity results in",ROOT)

if __name__=="__main__":
    main()
