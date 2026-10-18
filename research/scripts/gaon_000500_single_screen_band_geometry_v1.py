#!/usr/bin/env python3
"""Gaon Electric (000500) two INDEPENDENT single-screen five-band audits.

Input is manually seeded and visually reviewed pixel centers of original
screen captures (2026-05-11 and 2026-10-14), held privately by the user.
DO NOT mix image coordinates across captures.

May 11 screenshot: linear axis (P=(y-intercept)/slope);
Oct 14 screenshot: logarithmic axis (lnP=(y-intercept)/slope).
H0: constant log-price distance between top and each interior line, fit
on early samples; test y centers of late samples.
H1: constant fraction q of OBSERVED top-to-knee log price span at test x.
Thus H1 is only a conditional geometric reconstruction, NOT a predictor.

May uses dark indigo top-line candidate; Oct uses red top line; brown
super-top is excluded from both. No economic corporate-action comparison
is made here. All results are indicative due source 691px JPEG.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

ROOT=Path("research/results")
SOURCES=(
 ("2026-10-14","log",ROOT/"gaon_000500_20261014_single_screen_22_band_points_v1.csv",7),
 ("2026-05-11","linear",ROOT/"gaon_000500_20260511_single_screen_14_band_points_v1.csv",6),
)
TICKS=ROOT/"gaon_20260511_20261014_axis_tick_calibration_v1.csv"
MID=("shoulder_y_px","waist_y_px","thigh_y_px")

def fit(xs,ys):
    mx=sum(xs)/len(xs);my=sum(ys)/len(ys)
    a=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    b=my-a*mx
    err=math.sqrt(sum((y-(a*x+b))**2 for x,y in zip(xs,ys))/len(xs))
    return a,b,err

def load(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def rmse(values):
    assert values
    return math.sqrt(sum(x*x for x in values)/len(values))

def audit(root, ticks, date,mode,path,train_n):
    day_ticks=[r for r in ticks if r["snapshot_date"]==date]
    prices=[float(r["axis_price_krw"]) for r in day_ticks]
    pixels=[float(r["y_axis_tick_approx_px"]) for r in day_ticks]
    xx=[math.log(x) for x in prices] if mode=="log" else prices
    slope,intercept,axis_rmse=fit(xx,pixels)
    assert slope<0
    rows=load(root/path)
    assert len(rows)>train_n
    data=[]
    for r in rows:
        screen=[float(r[f]) for f in ("top_band_y_px",*MID,"knee_y_px")]
        if mode=="log":
            lp=[(y-intercept)/slope for y in screen]
        else:
            lp=[math.log((y-intercept)/slope) for y in screen]
        gap=lp[0]-lp[-1]
        assert gap>0
        data.append({"x":int(r["x_px"]),"y":screen,"logp":lp,"width":gap})
    assert [r["x"] for r in data]==sorted(set(r["x"] for r in data))
    first,last=data[0],data[-1]
    band_results=[];errors0=[];errors1=[]
    for mid_idx,name in enumerate(MID,1):
        train=data[:train_n];test=data[train_n:]
        train_gap=[r["logp"][0]-r["logp"][mid_idx] for r in train]
        offset=sum(train_gap)/len(train_gap)
        q=sum(g*r["width"] for g,r in zip(train_gap,train))/sum(r["width"]**2 for r in train)
        e0=[];e1=[]
        for r in test:
            lp0=r["logp"][0]-offset
            lp1=r["logp"][0]-q*r["width"]
            if mode=="log":
                pred0=intercept+slope*lp0
                pred1=intercept+slope*lp1
            else:
                pred0=intercept+slope*math.exp(lp0)
                pred1=intercept+slope*math.exp(lp1)
            e0.append(r["y"][mid_idx]-pred0)
            e1.append(r["y"][mid_idx]-pred1)
        errors0.extend(e0);errors1.extend(e1)
        band_results.append({"band":name,"train_offset_log":offset,"train_q":q,
                             "rmse_h0_px":rmse(e0),"rmse_h1_px":rmse(e1)})
    q_values=[]
    for band_idx in (1,2,3):
        q_values.append(sum((r["logp"][0]-r["logp"][band_idx])/r["width"] for r in data)/len(data))
    return {
      "snapshot_date":date,"mode":mode,"axis_slope":slope,
      "axis_intercept":intercept,"tick_rmse_px":axis_rmse,
      "n_points":len(data),"train_points":train_n,
      "test_points":len(data)-train_n,"measured_band_test_count":len(errors0),
      "ratio_first":math.exp(first["width"]),"ratio_last":math.exp(last["width"]),
      "ratio_increase_pct":100*(math.exp(last["width"]-first["width"])-1),
      "top_knee_screen_width_first_px":first["y"][-1]-first["y"][0],
      "top_knee_screen_width_last_px":last["y"][-1]-last["y"][0],
      "q_mean":q_values,
      "rmse_h0_px":rmse(errors0),"rmse_h1_px":rmse(errors1),
      "bands":band_results
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("."))
    args=p.parse_args()
    ticks=load(args.root/TICKS)
    result=[audit(args.root,ticks,*record) for record in SOURCES]
    by_date={r["snapshot_date"]:r for r in result}
    assert abs(by_date["2026-10-14"]["rmse_h0_px"]-2.6981979)<0.001
    assert abs(by_date["2026-10-14"]["rmse_h1_px"]-4.1568986)<0.001
    assert abs(by_date["2026-05-11"]["rmse_h0_px"]-1.9715839)<0.001
    assert abs(by_date["2026-05-11"]["rmse_h1_px"]-2.7680392)<0.001
    print(json.dumps({"test":"screen geometry only, NOT stock price prediction",
                      "screens":result},indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
