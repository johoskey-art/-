#!/usr/bin/env python3
"""Independent Aug-07-2026 SK Hynix FIVE band geometry, single screenshot.

Manual/HSV-supported original JPEG pixel centers in the source CSV. The
image is private in the user's ChatGPT file Library, not distributed here.

H0: same fixed log-offset between each middle band and red band;
H1: each middle band's log-offset is q_i * OBSERVED red-to-blue width.
      H1 reconstructs shapes using test-window red and blue values:
      it is NOT a future predictor of red/blue levels or profits.
TRANSFER: 2026-07-28 q_i frozen on that screenshot, tested without re-fit
          on the 2026-08-07 screenshot.
Measurements hidden by candles/text are empty, never interpolated for score.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

DEFAULT = Path("research/results/skh_20260807_single_screen_five_band_independent_v1.csv")
JULY = Path("research/results/skh_20260728_3year_five_band_models_holdout_v1.json")
FIELDS = ("green_shoulder_y_px", "black_waist_y_px", "orange_thigh_y_px")

def load(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        values=list(csv.DictReader(f))
    assert len(values)==14, "expected 14 samples; audit if version changes"
    result=[]
    for a in values:
        r={"x":int(a["x_px"])}
        for k in ("red_top_y_px","blue_knee_y_px",*FIELDS):
            r[k] = float(a[k]) if a[k] else None
        r["w"]=r["blue_knee_y_px"]-r["red_top_y_px"] if r["red_top_y_px"] is not None else None
        if r["w"] is not None: assert r["w"]>0
        result.append(r)
    assert [r["x"] for r in result]==sorted(set(r["x"] for r in result))
    return result

def rmse(residuals):
    assert residuals
    return math.sqrt(sum(x*x for x in residuals)/len(residuals))

def compare(rows, july):
    train,test=rows[:6],rows[6:]
    old={x["band"]:float(x["train_q"]) for x in july["intermediate_bands"]["per_band"]}
    squared={"H0":[],"H1":[],"JulyQ":[]}
    detail=[]
    for band in FIELDS:
        def values(rs):
            return [(r[band]-r["red_top_y_px"],r["w"]) for r in rs
                    if r["red_top_y_px"] is not None and r[band] is not None]
        a,b=values(train),values(test)
        offset=sum(d for d,w in a)/len(a)
        q=sum(d*w for d,w in a)/sum(w*w for d,w in a)
        err0=[d-offset for d,w in b]
        err1=[d-q*w for d,w in b]
        errtransfer=[d-old[band]*w for d,w in b]
        squared["H0"].extend(err0)
        squared["H1"].extend(err1)
        squared["JulyQ"].extend(errtransfer)
        detail.append({"band":band,"train_n":len(a),"test_n":len(b),
                       "q":round(q,5),"july_q":round(old[band],5),
                       "H0_rmse_px":round(rmse(err0),4),
                       "H1_rmse_px":round(rmse(err1),4),
                       "JulyQ_rmse_px":round(rmse(errtransfer),4)})
    n=len(squared["H0"]);assert n==17
    first,last=rows[0],rows[-1]
    assert first["w"]==108 and last["w"]==122
    beta=75.02
    widths=first["w"],last["w"]
    return {"sample_count":len(rows),"test_band_measurements":n,
            "ratio_first":round(math.exp(widths[0]/beta),5),
            "ratio_last":round(math.exp(widths[1]/beta),5),
            "width_delta_px":widths[1]-widths[0],
            "uncertainty_delta_each_band_endpoint_pm2":[(widths[1]-widths[0])-8,(widths[1]-widths[0])+8],
            "uncertainty_delta_each_band_endpoint_pm4":[(widths[1]-widths[0])-16,(widths[1]-widths[0])+16],
            "RMSE_H0":round(rmse(squared["H0"]),4),
            "RMSE_H1":round(rmse(squared["H1"]),4),
            "RMSE_July28FrozenQ":round(rmse(squared["JulyQ"]),4),
            "per_band":detail}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,default=DEFAULT)
    ap.add_argument("--july",type=Path,default=JULY)
    args=ap.parse_args()
    result=compare(load(args.input),json.loads(args.july.read_text(encoding="utf-8")))
    assert abs(result["RMSE_H0"]-3.5276)<0.0001
    assert abs(result["RMSE_H1"]-0.9280)<0.0001
    assert abs(result["RMSE_July28FrozenQ"]-2.4569)<0.0001
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("CAUTION: this is image geometry reconstruction, NOT prediction.")

if __name__=="__main__":main()
