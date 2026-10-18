#!/usr/bin/env python3
"""Original SK Hynix chart geometry pilot (screen pixels; NOT band price data).

Two user-provided SKHynix screenshots recovered from their private Library:
2026-07-28 1000008432(1).jpg, 2026-08-07 1000008429.jpg.
Manually read line-center y pixels and price-axis y tick coordinates.
Do not confuse observational screenshot date s with band historical t.
Coordinates are exploratory, expected visual errors +-2~4 pixels.
This script is deterministic and uses no network and no price series.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

DEFAULT = Path("research/results/skh_band_geometry_two_captures_manual_pixels_v1.csv")
# Price labels at y pixels in the original 691x1536 charts.
TICKS = {
    "2026-08-07": [(2_000_000,674), (1_000_000,724), (500_000,778)],
    "2026-07-28": [(2_000_000,660), (1_000_000,704), (500_000,750)],
}

def log_axis_beta(ticks):
    x=[math.log(price/1e6) for price,y in ticks]
    y=[float(pixel) for price,pixel in ticks]
    mx=sum(x)/len(x); my=sum(y)/len(y)
    m=sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)
    assert m < 0
    return -m

def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DEFAULT)
    args=ap.parse_args()
    with args.input.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh))
    assert len(rows)==4
    for r in rows:
        date=r["capture_date"]
        beta=log_axis_beta(TICKS[date])
        y_top=int(r["red_top_y_px"])
        y_knee=int(r["blue_knee_y_px"])
        ratio=math.exp((y_knee-y_top)/beta)
        assert abs(beta-float(r["axis_beta_px_per_ln"]))<0.005
        assert abs(ratio-float(r["top_to_knee_ratio_approx"]))<0.002
        print(f"{date} {r['approx_period']} x={r['x_original_px']}"
              f" pixels_top_to_knee={y_knee-y_top} beta={beta:.3f}"
              f" estimated_top_over_knee={ratio:.3f}")
    jan=float(rows[0]["top_to_knee_ratio_approx"])
    jul=float(rows[2]["top_to_knee_ratio_approx"])
    p_jan=int(rows[0]["top_to_knee_gap_px"])
    p_jul=int(rows[2]["top_to_knee_gap_px"])
    print(f"2026-08-07 screenshot Jan->Jul pixel expansion: "
          f"{p_jul-p_jan} px; ratio proxy {jan:.3f}->{jul:.3f}; "
          f"relative expansion {(jul/jan-1)*100:.1f}%")
    # Deterministic sensitivity bound from 2px error on each endpoint
    # at EACH of two time samples: difference in two widths has +/-8px.
    lo=(p_jul-p_jan)-8
    hi=(p_jul-p_jan)+8
    print(f"Endpoint +/-2 px worst-case gap expansion: [{lo},{hi}] px")
    print("No conclusion on original band coefficients or manual adjustments.")

if __name__=="__main__":
    main()
