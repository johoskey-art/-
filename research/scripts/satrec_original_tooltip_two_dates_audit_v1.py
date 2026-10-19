#!/usr/bin/env python3
"""Verify exact-looking numeric five-band TOOLTIP prices in two historical
dates, directly read from two user-owned retrospective Satrec chart JPGs.

IMPORTANT: source screenshots were recorded/recovered in 2026; 2021-03-29
is the historical cursor date, NOT a screenshot saved in 2021.
Line indicator label on both screenshots is '주가위치2'.
Do not confuse tooltip index 4 (waist) with level-order index.
Do not infer proprietary original Fibonacci formula.
"""
import argparse
import csv
import json
import math
from pathlib import Path

DEFAULT = Path("research/results/satrec_099320_original_tooltip_2dates_5bands_v1.csv")
EXPECTED = {"2021-03-29", "2026-02-04"}
ORDER = ("knee", "thigh", "waist", "shoulder", "top")
INDEX = {"knee":0, "thigh":1, "waist":4, "shoulder":2, "top":3}

def read(path):
    snapshots={}
    with path.open(encoding="utf-8-sig", newline="") as h:
        for r in csv.DictReader(h):
            assert r["ticker"]=="099320"
            date=r["date"];band=r["band"]
            assert int(r["tooltip_indicator_index"])==INDEX[band]
            assert band not in snapshots.setdefault(date,{})
            snapshots[date][band]=float(r["displayed_price_krw"])
    assert set(snapshots)==EXPECTED
    for snap in snapshots.values():
        assert set(snap)==set(ORDER)
        assert all(snap[ORDER[i]]<snap[ORDER[i+1]] for i in range(len(ORDER)-1))
    assert snapshots["2021-03-29"]["shoulder"]==91855.15
    return snapshots

def qlog(v,band):
    return math.log(v["top"]/v[band])/math.log(v["top"]/v["knee"])

def qlinear(v,band):
    return (v["top"]-v[band])/(v["top"]-v["knee"])

def interpolate_log(v,q):
    return math.exp((1-q)*math.log(v["top"])+q*math.log(v["knee"]))

def relative_error(pred,actual):
    return 100*(pred/actual-1)

def calculate(s):
    prior=s["2021-03-29"];later=s["2026-02-04"]
    within=[]
    for date in sorted(s):
        v=s[date]
        q=qlog(v,"thigh")
        original=v["thigh"]
        within.append({
          "date":date,
          "thigh_qlog":q,
          "thigh_qarithmetic":qlinear(v,"thigh"),
          "top_over_knee":v["top"]/v["knee"],
          "log_5over7_error_pct":relative_error(interpolate_log(v,5/7),original),
          "log_0p72_error_pct":relative_error(interpolate_log(v,0.72),original),
        })
    transfers=[]
    for band in ("shoulder","waist","thigh"):
        q=qlog(prior,band)
        qlinear_prior=qlinear(prior,band)
        pred_log=interpolate_log(later,q)
        pred_linear=later["top"]-qlinear_prior*(later["top"]-later["knee"])
        transfers.append({
          "band":band,"frozen_2021_log_q":q,
          "observed_2026_log_q":qlog(later,band),
          "frozen_2021_arithmetic_q":qlinear_prior,
          "observed_2026_arithmetic_q":qlinear(later,band),
          "2026_observed_krw":later[band],
          "2026_pred_from_frozen_logq_krw":pred_log,
          "2026_pred_from_frozen_linearq_krw":pred_linear,
          "2026_frozen_logq_error_pct":relative_error(pred_log,later[band]),
          "2026_frozen_linearq_error_pct":relative_error(pred_linear,later[band])
        })
    assert max(abs(x["2026_frozen_logq_error_pct"]) for x in transfers)<0.11
    assert all(x["log_5over7_error_pct"]<-1 for x in within)
    return {
      "source":"visually verified original 주가위치2 tooltip displayed figures",
      "retrospective_screens_not_live_2021":True,
      "within_dates":within,
      "frozen_internal_q_2021_to_2026_with_2026_top_knee_as_inputs":transfers,
      "caveat":"frozen log & linear q both fit due stable P/K; not proof of true formula."
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,default=DEFAULT)
    args=ap.parse_args()
    print(json.dumps(calculate(read(args.source)),ensure_ascii=False,indent=2))
