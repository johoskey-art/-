#!/usr/bin/env python3
"""SK Hynix 2026-07-28 *single-screen* 5-band geometry comparison.

Data source is manual/Hue-assisted pixel centers from the user's proprietary
blog screenshot 1000008432(1).jpg, original 691x1536 image.
This source image is NOT distributed in the public GitHub repository.
Do not treat image-line implied prices as official OHLCV or a trading signal.

H0: all red-relative offsets in log-price pixel space fixed over time.
H1: offsets to three interior bands = q_i * observed total red-blue width;
    q_i fitted on first six x columns (<=285) only. Blue is used to define
    width and MUST NOT be counted as a predictive test of H1.
H2: unrestricted time-varying q_i: saturated without adequate holdout,
    not fit/reported here.

Test is spatial reconstruction of screenshot *shape*, NOT temporal forecasting.
"""
from __future__ import annotations
import argparse
import csv
from math import exp, sqrt
from pathlib import Path

DEFAULT = Path("research/results/skh_20260728_3year_five_band_geometry_samples_v1.csv")
FIELDS = ("green_shoulder_y_px", "black_waist_y_px", "orange_thigh_y_px")
TRAIN_X_MAX = 285
BETA = 64.921

def read_records(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    result = []
    for row in rows:
        r = {"x": int(row["x_px"]), "red": float(row["red_top_y_px"]),
             "blue": float(row["blue_knee_y_px"])}
        for name in FIELDS:
            r[name] = float(row[name]) if row[name] else None
        r["width"] = r["blue"] - r["red"]
        assert r["width"] > 0
        result.append(r)
    assert len(result) == 17
    assert [r["x"] for r in result] == sorted(set(r["x"] for r in result))
    return result

def run(rows):
    train = [r for r in rows if r["x"] <= TRAIN_X_MAX]
    test = [r for r in rows if r["x"] > TRAIN_X_MAX]
    assert len(train) == 6 and len(test) == 11
    total_sq0 = total_sq1 = 0.
    n = 0
    parameters = []
    for band in FIELDS:
        a = [(r[band] - r["red"], r["width"]) for r in train if r[band] is not None]
        b = [(r[band] - r["red"], r["width"]) for r in test if r[band] is not None]
        d0 = sum(y for y,w in a)/len(a)
        q = sum(y*w for y,w in a)/sum(w*w for y,w in a)
        err0 = [(y-d0)**2 for y,w in b]
        err1 = [(y-q*w)**2 for y,w in b]
        total_sq0 += sum(err0); total_sq1 += sum(err1); n += len(b)
        parameters.append({"band":band,"train_n":len(a),"test_n":len(b),
                           "fixed_offset_px":round(d0,4),"fixed_q":round(q,5),
                           "rmse_H0_test_px":round(sqrt(sum(err0)/len(err0)),4),
                           "rmse_H1_test_px":round(sqrt(sum(err1)/len(err1)),4)})
    first,last=rows[0],rows[-1]
    delta = last["width"]-first["width"]
    assert delta > 0 and n == 27
    return {
        "source":"original_2026-07-28_SKH_user_screenshot",
        "observations":len(rows),"first_x":first["x"],"last_x":last["x"],
        "width_start_px":round(first["width"],3),
        "width_end_px":round(last["width"],3),
        "width_increase_px":round(delta,3),
        "red_over_blue_start_est":round(exp(first["width"]/BETA),4),
        "red_over_blue_end_est":round(exp(last["width"]/BETA),4),
        "relative_growth_pct":round(100*(exp(delta/BETA)-1),2),
        "delta_width_px_error_bound_at_each_center_plusminus2":
           [round(delta-8,2),round(delta+8,2)],
        "delta_width_px_error_bound_at_each_center_plusminus4":
           [round(delta-16,2),round(delta+16,2)],
        "tested_intermediate_measurements":n,
        "rmse_H0_spatial_holdout_px":round(sqrt(total_sq0/n),4),
        "rmse_H1_spatial_holdout_px":round(sqrt(total_sq1/n),4),
        "bands":parameters,
        "interpretation":"H1 better spatial fit. No source proof of original indicator formula; no ability to say manual vs auto or future performance."
    }

if __name__=="__main__":
    import json
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=DEFAULT)
    args=ap.parse_args()
    print(json.dumps(run(read_records(args.input)),ensure_ascii=False,indent=2))
