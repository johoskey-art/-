#!/usr/bin/env python3
"""Study extension: US holdout TSLA/NVDA and prior-2y-high anchor, v1.
Usage: python research/scripts/us_holdout_anchor_v1.py
Writes CSV files in research/results/. Downloads pinned GitHub source commits.
Outputs are RETROSPECTIVE, not real-time predictions.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import statistics
import urllib.request
from datetime import date
from pathlib import Path

from split_cycles_v1 import CASES as KOREA_CASES, SOURCE_COMMIT as KOREA_COMMIT
from split_cycles_v1 import SOURCE_REPO as KOREA_REPO

ROOT = Path("research/results")
US_CASES = [
    dict(
        name="Tesla", ticker="TSLA",
        start="2020-03-01", end="2021-12-31",
        repo="HassanJamel/Tesla-TSLA-Comprehensive-Exploratory-Data-Analysis",
        path="TSLA.csv",
        commit="c385e8d975f72c71211d9ac54f8dd92f6d6d1382",
        sha="a2a37425f2d3cd64a3e40ee2ade31dd7d946a243",
    ),
    dict(
        name="NVIDIA", ticker="NVDA",
        start="2022-10-01", end="2024-07-31",
        repo="kalilurrahman/NVidiaStockdata", path="NVidia_stock_history.csv",
        commit="5f1f37cf7ded02684baf7571857c2156ccc32362",
        sha="1cc301dfa80ce5045704ffb350a788db761d9936",
    ),
]

SPLIT_COLUMNS = [
    "symbol","ticker","case_start","case_end","observed_start",
    "observed_peak","P0_close","PH_close","trading_days","split_axis",
    "price_scale","k","j","j_over_k","observed_date","observed_close",
    "price_position","elapsed_position","threshold_close","source_blob_sha",
]

ANCHOR_COLUMNS = [
    "name","ticker","episode_low_date","episode_low_close","peak_date",
    "peak_close","prior_two_year_max_date","prior_two_year_max_close",
    "prior_obs","low_over_previous_high","peak_over_previous_high",
    "previous_high_in_total_rise","first_crossover_fraction",
    "first_crossover_date","source_sha","source_repo",
]

def fetch_source(c):
    url = ("https://raw.githubusercontent.com/" + c["repo"] + "/"
           + c["commit"] + "/" + c["path"])
    with urllib.request.urlopen(url, timeout=60) as f:
        data = f.read()
    actual = hashlib.sha1((f"blob {len(data)}\0").encode() + data).hexdigest()
    if actual != c["sha"]:
        raise RuntimeError(f"{c['ticker']} SOURCE MISMATCH: {actual}, expected {c['sha']}")
    return data

def normalize_date(s):
    s = s[:10]
    if "/" in s:
        month, day, year = s.split("/")
        return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return s

def source_rows(data):
    res = []
    for r in csv.DictReader(io.StringIO(data.decode("utf-8-sig"))):
        try:
            p = dict(
                date=normalize_date(r["Date"]),
                close=float(r["Close"]),
                high=float(r["High"]),
                low=float(r["Low"]),
            )
        except (KeyError, ValueError, TypeError):
            continue
        if p["close"] > 0:
            res.append(p)
    res.sort(key=lambda x: x["date"])
    return res

def episode(rows, c):
    search = [p for p in rows if c["start"] <= p["date"] <= c["end"]]
    if not search:
        raise ValueError(c["ticker"] + ": no observations")
    lo = min(search, key=lambda x: x["close"])
    eligible = [p for p in search if p["date"] >= lo["date"]]
    # Earliest date on ties (preserve chronological sorted ordering).
    hi = max(eligible, key=lambda x: x["close"])
    series = [p for p in eligible if p["date"] <= hi["date"]]
    if len(series) < 10 or hi["close"] <= lo["close"]:
        raise ValueError(c["ticker"] + ": invalid episode")
    bad = sum(not p["low"]-1e-5 <= p["close"] <= p["high"]+1e-5 for p in series)
    return lo, hi, series, bad

def splits(c, lo, hi, series):
    n = len(series)-1
    for k in (5, 7):
        for axis in ("time","price"):
            for scale in ("linear","log"):
                for j in range(k+1):
                    f = j/k
                    threshold = None
                    if axis == "time":
                        idx = math.floor(f*n+0.5)
                    else:
                        threshold = (lo["close"]+(hi["close"]-lo["close"])*f
                           if scale == "linear"
                           else lo["close"]*(hi["close"]/lo["close"])**f)
                        idx = next((i for i,p in enumerate(series)
                                    if p["close"] >= threshold-1e-9),-1)
                        if idx < 0:
                            raise ValueError(c["ticker"] + " threshold not reached")
                    x = series[idx]
                    q = ((x["close"]-lo["close"])/(hi["close"]-lo["close"])
                         if scale == "linear"
                         else math.log(x["close"]/lo["close"]) /
                              math.log(hi["close"]/lo["close"]))
                    yield dict(
                        symbol=c["name"],ticker=c["ticker"],case_start=c["start"],
                        case_end=c["end"],observed_start=lo["date"],observed_peak=hi["date"],
                        P0_close=f"{lo['close']:.6f}",PH_close=f"{hi['close']:.6f}",
                        trading_days=len(series),split_axis=axis,price_scale=scale,
                        k=k,j=j,j_over_k=f"{f:.6f}",observed_date=x["date"],
                        observed_close=f"{x['close']:.6f}",price_position=f"{q:.6f}",
                        elapsed_position=f"{idx/n:.6f}",
                        threshold_close=("" if threshold is None else f"{threshold:.6f}"),
                        source_blob_sha=c["sha"],
                    )

def years_before(d: str, n: int=2):
    y,m,day = (int(z) for z in d.split("-"))
    try:
        return date(y-n,m,day).isoformat()
    except ValueError:
        return date(y-n,m,28).isoformat()

def anchor_row(c, rows, lo, hi, series):
    # IMPORTANT: 2-year trailing maximum is a PROXY, not confirmed prior-cycle peak.
    trailing = [p for p in rows if years_before(lo["date"]) <= p["date"] < lo["date"]]
    if len(trailing) < 250:
        raise ValueError(c["ticker"] + ": under 250 prior observations")
    prev = max(trailing,key=lambda x: x["close"])
    idx = next((i for i,p in enumerate(series) if p["close"] >= prev["close"]),-1)
    return dict(
        name=c["name"],ticker=c["ticker"],episode_low_date=lo["date"],
        episode_low_close=f"{lo['close']:.6f}",peak_date=hi["date"],
        peak_close=f"{hi['close']:.6f}",prior_two_year_max_date=prev["date"],
        prior_two_year_max_close=f"{prev['close']:.6f}",prior_obs=len(trailing),
        low_over_previous_high=f"{lo['close']/prev['close']:.6f}",
        peak_over_previous_high=f"{hi['close']/prev['close']:.6f}",
        previous_high_in_total_rise=f"{(prev['close']-lo['close'])/(hi['close']-lo['close']):.6f}",
        first_crossover_fraction=("" if idx<0 else f"{idx/(len(series)-1):.6f}"),
        first_crossover_date=("" if idx<0 else series[idx]["date"]),
        source_sha=c["sha"],source_repo=c["repo"],
    )

def save_csv(path,cols,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols)
        writer.writeheader()
        writer.writerows(records)

def main():
    original = [
        dict(name=name,ticker=ticker,start=t0,end=t1,
             repo=KOREA_REPO,commit=KOREA_COMMIT,
             path=f"Korea_Stocks_Full/{ticker}.csv",sha=sha)
        for name,ticker,t0,t1,sha in KOREA_CASES
    ]
    us_rows, anchors, us_episodes = [], [], []
    for c in original+US_CASES:
        rows = source_rows(fetch_source(c))
        lo, hi, series, bad = episode(rows,c)
        anchors.append(anchor_row(c,rows,lo,hi,series))
        if c in US_CASES:
            us_episodes.append(dict(stock=c["name"],ticker=c["ticker"],
                case_window=c["start"]+".."+c["end"],
                start_date=lo["date"],low_close=f"{lo['close']:.6f}",
                peak_date=hi["date"],peak_close=f"{hi['close']:.6f}",
                gain_multiple=f"{hi['close']/lo['close']:.6f}",
                trading_days=len(series),ohlc_close_out_of_bounds_rows=bad,
                source_blob_sha=c["sha"],source_commit=c["commit"]))
            us_rows.extend(splits(c,lo,hi,series))
        print(c["ticker"],lo["date"],hi["date"],"X",f"{hi['close']/lo['close']:.2f}")
    save_csv(ROOT/"anchor_proxy_10_v1.csv",ANCHOR_COLUMNS,anchors)
    save_csv(ROOT/"us_holdout_splits_v1.csv",SPLIT_COLUMNS,us_rows)
    save_csv(ROOT/"us_holdout_episodes_v1.csv",
        list(us_episodes[0].keys()),us_episodes)
    print("Saved",len(anchors),"anchor episodes and",len(us_rows),"US split observations")

if __name__ == "__main__":
    main()
