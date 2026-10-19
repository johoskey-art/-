#!/usr/bin/env python3
"""SK Corp (034730) original 2026-07-28 chart fourth-stock out-of-sample test.

Prior to inspecting SK Corp, other stock charts suggested q_thigh≈5/7.
This script NEVER fits that q to SK Corp observations.

q_i=(y_i-y_red)/(y_blue-y_red) is equivalent to a normalized log-price
distance ONLY when the chart y-axis is logarithmic. Seven independently
read price ticks validate the log-axis approximation. Pixels/line labels
were manually seeded, HSV color-assisted, and overlaid for visual review.
Exclude the thick YELLOW handwritten trend line; actual orange thigh line
is thin and near 300k at the chart's left.

CAUTION: 21 x-columns on one screenshot are highly correlated. Never
treat these as 21 independent securities, exact indicator prices, or
evidence of the author's Fibonacci formula. Masked 'good' is subjective.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

DEFAULT=Path("research/results/sk_034730_20260728_frozen_5over7_band_samples_v1.csv")
TICKS=[(200000,810),(300000,766),(400000,734),(600000,696),
       (700000,680),(800000,667),(1000000,642)]
BANDS=("green_shoulder_y_px","black_waist_y_px","orange_thigh_y_px")
FROZEN=5/7

def linefit(xs,ys):
    mx=sum(xs)/len(xs);my=sum(ys)/len(ys)
    m=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    a=my-m*mx
    rmse=math.sqrt(sum((a+m*x-y)**2 for x,y in zip(xs,ys))/len(xs))
    return m,a,rmse

def rmse(e):
    assert e
    return math.sqrt(sum(v*v for v in e)/len(e))

def load(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        source=list(csv.DictReader(f))
    assert len(source)==21
    data=[]
    for z in source:
        o={"x":int(z["x_px"])}
        for key in ("red_top_y_px","blue_knee_y_px",*BANDS):
            o[key]=float(z[key])
        o["quality"]=(z["red_quality"],z["orange_quality"],z["blue_quality"])
        o["width"]=o["blue_knee_y_px"]-o["red_top_y_px"]
        o["q_thigh"]=(o["orange_thigh_y_px"]-o["red_top_y_px"])/o["width"]
        assert 0<o["q_thigh"]<1
        data.append(o)
    assert [r["x"] for r in data]==sorted(set(r["x"] for r in data))
    return data

def score_fixed(rows,ratio=FROZEN):
    e=[x["orange_thigh_y_px"]-
      (x["red_top_y_px"]+ratio*x["width"]) for x in rows]
    return {"n":len(rows),"q_mean":sum(x["q_thigh"] for x in rows)/len(rows),
            "q_median":sorted(x["q_thigh"] for x in rows)[len(rows)//2],
            "error_mae_px":sum(abs(z) for z in e)/len(e),
            "error_rmse_px":rmse(e),"error_bias_px":sum(e)/len(e)}

def score_geometry(rows,train_n=7):
    a,b=rows[:train_n],rows[train_n:]
    err0=[];err1=[]
    for name in BANDS:
        d=[r[name]-r["red_top_y_px"] for r in a]
        w=[r["width"] for r in a]
        fixed=sum(d)/len(d)
        q=sum(v*vwidth for v,vwidth in zip(d,w))/sum(vwidth**2 for vwidth in w)
        for r in b:
            observed=r[name]-r["red_top_y_px"]
            err0.append(observed-fixed)
            err1.append(observed-q*r["width"])
    return {"train_n":train_n,"holdout_interior_band_n":len(err0),
            "H0_fixed_top_offset_RMSE_px":rmse(err0),
            "H1_observed_total_width_RMSE_px":rmse(err1)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",type=Path,default=DEFAULT)
    args=p.parse_args()
    rows=load(args.csv)
    strict=[r for r in rows if r["quality"]==("good","good","good")]
    m,a,elog=linefit([math.log(p) for p,y in TICKS],[y for p,y in TICKS])
    _,_,elin=linefit([p for p,y in TICKS],[y for p,y in TICKS])
    assert elog<elin and len(strict)==6
    allscore=score_fixed(rows);strictscore=score_fixed(strict)
    assert abs(allscore["q_mean"]-0.7232763805649798)<1e-9
    assert abs(strictscore["q_mean"]-0.7216330285355118)<1e-9
    assert abs(allscore["error_rmse_px"]-1.7978742441733717)<1e-9
    geometry=score_geometry(rows,7)
    assert geometry["H1_observed_total_width_RMSE_px"] < geometry["H0_fixed_top_offset_RMSE_px"]
    before,after=rows[0]["width"],rows[-1]["width"]
    assert before==119 and after==141
    output={"ticker":"034730","axis_beta_px_per_log":-m,
            "axis_log_rmse_px":elog,"axis_linear_rmse_px":elin,
            "frozen_q":FROZEN,
            "all":allscore,"strict_good_colors":strictscore,
            "early":score_fixed(rows[:10]),"late":score_fixed(rows[10:]),
            "q_0p70":score_fixed(rows,.70)["error_rmse_px"],
            "q_0p72_POSTHOC":score_fixed(rows,.72)["error_rmse_px"],
            "q_0p75":score_fixed(rows,.75)["error_rmse_px"],
            "band_width_px":[before,after],
            "top_knee_rough_price_ratio":[math.exp(before/(-m)),math.exp(after/(-m))],
            "H0_H1_with_observed_endpoints":geometry}
    print(json.dumps(output,ensure_ascii=False,indent=2))
    print("Final verdict: 5/7 is compatible with JPEG precision, not identified as exact author's formula.")

if __name__=="__main__":main()
