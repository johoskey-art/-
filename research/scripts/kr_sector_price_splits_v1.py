#!/usr/bin/env python3
"""Domestic leader 5/7 PRICE partition summaries, offline and reproducible.

Inputs:
  research/results/kr_46_candidate_audit_v1.csv
Outputs:
  research/results/kr_30_clean_episodes_v1.csv
  research/results/kr_30_stage_summary_v1.csv

Does not need Internet. The source audit includes source file SHA for each episode.
DO NOT interpret original blogger's 5/7 method or Fibonacci formula as verified.
Statistical units are (company, PDF sector-leader year) episodes, not independent firms.

Run from repository root:
  python research/scripts/kr_sector_price_splits_v1.py
"""
from pathlib import Path
import csv
import math
import statistics

DIR=Path("research/results")
AUDIT=DIR/"kr_46_candidate_audit_v1.csv"
CLEAN=DIR/"kr_30_clean_episodes_v1.csv"
STAGES=DIR/"kr_30_stage_summary_v1.csv"
CLEAN_FIELDS=[
    "y","name","ticker","sector","low","low_close","peak","peak_close",
    "days","R","factor5","factor7","source_sha"
]
STAGE_FIELDS=[
    "split_k","step_j","relative_price_fraction",
    "geo_mean_price_over_low","geo_median_price_over_low",
    "linear_mean_price_over_low","linear_median_price_over_low",
    "mean_price_step_multiplier","median_price_step_multiplier","n"
]

def load():
    with AUDIT.open("r",newline="",encoding="utf-8") as f:
        source=list(csv.DictReader(f))
    if len(source)!=46:
        raise RuntimeError(f"expected 46 frozen episodes, got {len(source)}")
    records=[]
    for row in source:
        if row["status"]!="ELIGIBLE":
            continue
        lo=float(row["cycle_low_close"])
        hi=float(row["peak_close"])
        r=hi/lo
        # AUDIT R is the raw computed price multiple, verify it before deriving any factors.
        if lo<=0 or hi<=lo or not math.isclose(r,float(row["R_total"]),rel_tol=1e-10):
            raise RuntimeError(f"invalid source multiple {row['ticker']}:{row['cohort_year']}")
        records.append(dict(
            y=int(row["cohort_year"]),name=row["pdf_stock_name"],ticker=row["ticker"],
            sector=row["sector"],low=row["cycle_low_date"],
            low_close=lo,peak=row["peak_date"],peak_close=hi,
            days=int(row["days_low_to_peak"]),R=r,
            factor5=r**(1/5),factor7=r**(1/7),
            source_sha=row["source_sha"]
        ))
    if len(records)!=30:
        raise RuntimeError(f"expected 30 clean episodes, got {len(records)}")
    return records

def stages(records):
    result=[]
    for k in (5,7):
        steps=[r["R"]**(1/k) for r in records]
        for j in range(k+1):
            geom=[r["R"]**(j/k) for r in records]
            linear=[1+(r["R"]-1)*j/k for r in records]
            result.append(dict(
                split_k=k,step_j=j,relative_price_fraction=j/k,
                geo_mean_price_over_low=statistics.mean(geom),
                geo_median_price_over_low=statistics.median(geom),
                linear_mean_price_over_low=statistics.mean(linear),
                linear_median_price_over_low=statistics.median(linear),
                mean_price_step_multiplier=statistics.mean(steps),
                median_price_step_multiplier=statistics.median(steps),
                n=len(records)
            ))
    return result

def write(path, columns, values):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=columns);wr.writeheader();wr.writerows(values)

def main():
    records=load()
    summary=stages(records)
    write(CLEAN,CLEAN_FIELDS,records)
    write(STAGES,STAGE_FIELDS,summary)
    for k in (5,7):
        vals=[r[f"factor{k}"] for r in records]
        print(k,"segments, n=",len(vals),
              "mean=",round(statistics.mean(vals),9),
              "median=",round(statistics.median(vals),9))
    by_sector={}
    for r in records:
        by_sector.setdefault(r["sector"],[]).append(r["factor5"])
    sector_balanced=statistics.mean(statistics.mean(v) for v in by_sector.values())
    print("sector-balanced 5-segment mean:",round(sector_balanced,9))
    print("wrote:",CLEAN,"and",STAGES)

if __name__=="__main__":
    main()
