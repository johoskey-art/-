#!/usr/bin/env python3
"""Samsung Electro-Mechanics (009150) third-stock band geometry audit.

Reproduces a 21-x original JPEG screenshot pixel study, 2026-10-14.
Source JPEG is in the user's personal Library, not uploaded to GitHub.
This is image geometry reconstruction, never a future-price prediction.
H0: for each middle band, fixed red-relative log gap (pixel y offset).
H1: each middle band occupies fixed proportion of OBSERVED red-blue gap.
H1 has extra test-time observed blue endpoint. Do not claim prediction.
Color centers are manually seeded, HSV-refined with low-contrast black NA.
"""
from __future__ import annotations
import csv, math, argparse, json, statistics
from pathlib import Path

DEFAULT=Path("research/results/sem_009150_20261014_five_band_pixels_v1.csv")
BANDS=["green_shoulder_y_px","black_waist_y_px","orange_thigh_y_px"]
TICKS=[(500000,793),(1000000,751),(1500000,730),(2000000,705),
       (2500000,690),(3000000,680),(3500000,673),(4000000,665)]

def line_fit(xs, ys):
    mx=statistics.mean(xs);my=statistics.mean(ys)
    slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    intercept=my-slope*mx
    error=math.sqrt(statistics.mean((intercept+slope*x-y)**2 for x,y in zip(xs,ys)))
    return slope,intercept,error

def read(path):
    with path.open(encoding="utf-8-sig",newline="") as h:rows=list(csv.DictReader(h))
    assert len(rows)==21, "21 source x samples expected"
    out=[]
    for r in rows:
        obj={"x":int(r["x_px"]),"red":float(r["red_top_y_px"]),
             "blue":float(r["blue_knee_y_px"])}
        obj["width"]=obj["blue"]-obj["red"]
        assert obj["width"]>0
        for label,field in zip(("green","black","orange"),BANDS):
            obj[label]=float(r[field]) if r[field] else None
        out.append(obj)
    assert [z["x"] for z in out]==sorted(set(z["x"] for z in out))
    return out

def rmse(v):
    assert v
    return math.sqrt(statistics.mean(z*z for z in v))

def fit_models(samples,ntrain=8,use_black=True, max_x=1000):
    assert 5<=ntrain<=11
    train=samples[:ntrain];test=[z for z in samples[ntrain:] if z["x"]<=max_x]
    errors0=[];errors1=[];per=[]
    for label in ("green","black","orange"):
        if label=="black" and not use_black:continue
        tr=[z for z in train if z[label] is not None]
        te=[z for z in test if z[label] is not None]
        assert len(tr)>=3 and len(te)>=5
        y=[z[label]-z["red"] for z in tr]
        w=[z["width"] for z in tr]
        offset=statistics.mean(y)
        q=sum(a*b for a,b in zip(y,w))/sum(b*b for b in w)
        e0=[z[label]-(z["red"]+offset) for z in te]
        e1=[z[label]-(z["red"]+q*z["width"]) for z in te]
        errors0.extend(e0);errors1.extend(e1)
        q_full=[(z[label]-z["red"])/z["width"] for z in samples if z[label] is not None]
        per.append({"name":label,"train_n":len(tr),"test_n":len(te),
                    "train_q":q,"full_screen_q_mean":statistics.mean(q_full),
                    "rmse_h0":rmse(e0),"rmse_h1":rmse(e1)})
    return {"train":len(train),"test":len(test),"test_middle_band_n":len(errors0),
            "rmse_h0":rmse(errors0),"rmse_h1":rmse(errors1),"per_band":per}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv",type=Path,default=DEFAULT)
    args=ap.parse_args()
    pts=read(args.csv)
    slope,intercept,tick_rmse=line_fit([math.log(price) for price,y in TICKS],[y for price,y in TICKS])
    _,_,linear_rmse=line_fit([price for price,y in TICKS],[y for price,y in TICKS])
    assert slope<0 and tick_rmse<linear_rmse
    w0=pts[0]["width"];w1=pts[-1]["width"]
    metrics=fit_models(pts,8)
    assert len(pts)==21 and metrics["test_middle_band_n"]==39
    assert abs(metrics["rmse_h0"]-7.652011843718634)<0.0001
    assert abs(metrics["rmse_h1"]-1.2528623148999187)<0.0001
    print(json.dumps({"ticker":"009150","source_screen_date":"2026-10-14",
     "axis_beta_px_per_ln":-slope,"axis_tick_fit_rmse_px":tick_rmse,
     "start_width_px":w0,"end_width_px":w1,
     "top_knee_ratio_start":math.exp(w0/(-slope)),
     "top_knee_ratio_end":math.exp(w1/(-slope)),
     "fixed_train8_model_comparison":metrics,
     "alternate_train_sizes":[fit_models(pts,n) for n in (6,7,9,10,11)],
     "exclude_black_line":fit_models(pts,8,use_black=False)},
     indent=2,ensure_ascii=False))
    print("CAUTION: spatial JPEG screen shape only, NOT original line values or future forecasts.")

if __name__=="__main__":main()
