#!/usr/bin/env python3
"""주가위치 탐색기 — 사후 5/7등분 재현 실험 v1.
Run: python research/scripts/split_cycles_v1.py
Uses pinned public source CSVs; requires network. No trading signals.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import math
import statistics
import urllib.request
from pathlib import Path

SOURCE_REPO = "choosunsick/Korea_Stocks"
SOURCE_COMMIT = "0aec8dc0ce335a3a15fa23ec1c853137f0d9ca3a"
# source blobs verified in GitHub connector on 2026-10-17
CASES = [
    ("현대차", "005380", "2008-10-01", "2011-06-30", "c47ab7d6ce338adfedb92e646cd1a409ee3bd07b"),
    ("기아", "000270", "2008-10-01", "2011-06-30", "f41d91c825b1f250c38ebea4d6ae8f7a1429b77f"),
    ("LG화학", "051910", "2008-10-01", "2011-06-30", "8704dafcd77fb03843825b2a5a6ab249b4cad070"),
    ("POSCO홀딩스", "005490", "2003-01-01", "2007-12-31", "3b827eb5b50b973128d577af5957d0a22f2d292f"),
    ("삼성중공업", "010140", "2003-01-01", "2007-12-31", "3d7ff5b0f8c3d9f637d7ee64b27a21aa426f3920"),
    ("삼성전자", "005930", "2016-01-01", "2017-12-31", "e7c42fdfd76e451107f521c683ef15637a77a39e"),
    ("SK하이닉스", "000660", "2016-01-01", "2018-08-31", "8c8bc6a6adda52ebd6b7f439200da3fad54b20bc"),
    ("한미약품", "128940", "2014-01-01", "2015-12-31", "e19d0f9295ffddbd3bdb3b5e4fca21ce7b1d21f3"),
]
SPLIT_FIELDS = [
    "symbol","ticker","case_start","case_end","observed_start",
    "observed_peak","P0_close","PH_close","trading_days","split_axis",
    "price_scale","k","j","j_over_k","observed_date","observed_close",
    "price_position","elapsed_position","threshold_close","source_blob_sha"
]
EPISODE_FIELDS = [
    "stock","ticker","case_window","start_date","low_close","peak_date",
    "peak_close","gain_multiple","trading_days","ohlc_close_out_of_bounds_rows",
    "source_blob_sha"
]

def get_csv_bytes(ticker: str, expected_sha: str, local_dir: Path | None) -> bytes:
    path = f"Korea_Stocks_Full/{ticker}.csv"
    if local_dir:
        data = (local_dir / (ticker + ".csv")).read_bytes()
    else:
        url = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{path}"
        with urllib.request.urlopen(url, timeout=25) as response:
            data = response.read()
    actual = hashlib.sha1((f"blob {len(data)}\0").encode() + data).hexdigest()
    if actual != expected_sha:
        raise RuntimeError(f"{ticker}: SOURCE_SHA_MISMATCH expected={expected_sha}, actual={actual}. Do not proceed.")
    return data

def read_prices(data: bytes, t0: str, t1: str):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    ans = []
    for r in reader:
        d = r["Date"]
        if not (t0 <= d <= t1):
            continue
        try:
            p = {"date": d, "c": float(r["Close"]), "h": float(r["High"]), "l": float(r["Low"])}
        except (ValueError, TypeError):
            continue
        if p["c"] > 0:
            ans.append(p)
    ans.sort(key=lambda z: z["date"])
    return ans

def split_case(name, ticker, t0, t1, sha, data):
    prices = read_prices(data, t0, t1)
    if not prices:
        raise ValueError(f"{name}: no prices")
    # Earliest occurrence on ties. Use terminal peak only after the chosen low.
    low_i = min(range(len(prices)), key=lambda j: prices[j]["c"])
    high_i = max(range(low_i, len(prices)), key=lambda j: (prices[j]["c"], -j))
    ep = prices[low_i:high_i+1]
    low, high = ep[0], ep[-1]
    if len(ep) < 10 or high["c"] <= low["c"]:
        raise ValueError(f"{name}: invalid retrospective episode")
    n = len(ep)-1
    errors = sum(not (r["l"] <= r["c"] <= r["h"]) for r in ep)
    episode = dict(
        stock=name,ticker=ticker,case_window=t0+".."+t1,start_date=low["date"],
        low_close=int(low["c"]),peak_date=high["date"],peak_close=int(high["c"]),
        gain_multiple=f"{high['c']/low['c']:.6f}",trading_days=len(ep),
        ohlc_close_out_of_bounds_rows=errors,source_blob_sha=sha
    )
    records = []
    for k in (5,7):
        for axis in ("time","price"):
            for scale in ("linear","log"):
                for j in range(k+1):
                    fraction = j/k
                    threshold = None
                    if axis == "time":
                        # Python round uses ties-to-even; use floor(n*frac+0.5) instead
                        idx = math.floor(fraction*n+0.5)
                    else:
                        threshold = (low["c"] + (high["c"]-low["c"])*fraction if scale == "linear"
                                     else low["c"] * (high["c"]/low["c"])**fraction)
                        idx = next((q for q, r in enumerate(ep) if r["c"] >= threshold-1e-9), -1)
                        if idx < 0:
                            raise RuntimeError(f"unreached threshold {name} {k} {j}")
                    p = ep[idx]
                    pos = ((p["c"]-low["c"])/(high["c"]-low["c"]) if scale == "linear"
                           else math.log(p["c"]/low["c"])/math.log(high["c"]/low["c"]))
                    records.append(dict(
                        symbol=name,ticker=ticker,case_start=t0,case_end=t1,
                        observed_start=low["date"],observed_peak=high["date"],
                        P0_close=int(low["c"]),PH_close=int(high["c"]),trading_days=len(ep),
                        split_axis=axis,price_scale=scale,k=k,j=j,
                        j_over_k=f"{fraction:.6f}",observed_date=p["date"],
                        observed_close=int(p["c"]),price_position=f"{pos:.6f}",
                        elapsed_position=f"{idx/n:.6f}",
                        threshold_close=("" if threshold is None else f"{threshold:.6f}"),
                        source_blob_sha=sha
                    ))
    return episode, records

def save(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--local-dir", type=Path, help="Directory with ORIGINAL verified ticker.csv files")
    parser.add_argument("--out-dir", type=Path, default=Path("research/results"))
    args=parser.parse_args()
    episodes, records = [], []
    for name,ticker,t0,t1,sha in CASES:
        ep, rr = split_case(name,ticker,t0,t1,sha,get_csv_bytes(ticker,sha,args.local_dir))
        episodes.append(ep)
        records.extend(rr)
        print(f"{name}: {ep['start_date']}→{ep['peak_date']} ×{ep['gain_multiple']} (n={ep['trading_days']})")
    save(args.out_dir/"episodes_v1_20261017.csv",EPISODE_FIELDS,episodes)
    save(args.out_dir/"pilot_v1_20261017.csv",SPLIT_FIELDS,records)
    print("WROTE:",len(episodes),"episodes;",len(records),"split rows.")
    for k in (5,7):
        selected = [r for r in records if r["k"] == k and r["split_axis"] == "time" and r["price_scale"] == "linear"]
        for j in range(1,k):
            vv=[float(r["price_position"]) for r in selected if r["j"]==j]
            print(f"k={k} j={j}: mean={statistics.mean(vv):.4f}, median={statistics.median(vv):.4f}")

if __name__=="__main__":
    main()
