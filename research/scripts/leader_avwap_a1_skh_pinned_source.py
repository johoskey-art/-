#!/usr/bin/env python3
"""AVWAP A1: historical SK Hynix (000660), reproducible pinned public CSV.

SOURCE historical 2022-08-18 .. 2025-09-18; archived third-party Investing
prices on GitHub, NOT official KRX. V strings such as 4.14M are rounded:
therefore AVWAP is an estimate, even with high decimal precision.
Synthetic missing-volume rows are excluded rather than assigned volume=0.
Nothing here proves the blogger's knee indicator == AVWAP.

Usage on a networked machine:
    python research/scripts/leader_avwap_a1_skh_pinned_source.py
    python research/scripts/leader_avwap_a1_skh_pinned_source.py --csv downloaded.csv
"""
import argparse
import csv
import io
import json
from datetime import date
from pathlib import Path
from urllib.request import urlopen

URL = ("https://raw.githubusercontent.com/fnskcjswo123/Stock_AI/"
       "dcfecd1111c4262f9606706a728b75b28909b323/bin/"
       "sk%20%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4%20csv/"
       "000660%20%EA%B3%BC%EA%B1%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%281%29.csv")
ANCHORS = ("2023-05-25", "2023-07-10", "2023-07-27")
CHECK = ("2023-07-27", "2023-12-28", "2024-06-03",
         "2024-12-30", "2025-03-31", "2025-09-18")

def parse_volume(token):
    s=token.strip().replace(",", "")
    if not s:
        return 0.
    mul=1e6 if s[-1]=="M" else 1e3 if s[-1]=="K" else 1.
    if mul!=1: s=s[:-1]
    return float(s)*mul

def read_bars(src):
    data=[]
    excluded=0
    for record in csv.DictReader(io.StringIO(src.lstrip("\ufeff"))):
        d="".join(record["날짜"].split())
        h=float(record["고가"].replace(",",""))
        l=float(record["저가"].replace(",",""))
        c=float(record["종가"].replace(",",""))
        v=parse_volume(record["거래량"])
        if v<=0 or min(l,c)<=0 or h<l:
            excluded+=1
            continue
        date.fromisoformat(d)
        data.append({"date":d,"h":h,"l":l,"c":c,"v":v,"tp":(h+l+c)/3})
    data.sort(key=lambda x:x["date"])
    assert len(data)==len({z["date"] for z in data}),"duplicate valid trading date"
    return data,excluded

def calculate(bars):
    indices={a:next(i for i,z in enumerate(bars) if z["date"]==a) for a in ANCHORS}
    acc={a:{"weighted":0.,"vol":0.,"unweighted":0.,"n":0} for a in ANCHORS}
    out=[];ema=None
    for i,z in enumerate(bars):
        ema=z["c"] if ema is None else ema+(2/121)*(z["c"]-ema)
        # Update ALL accumulators at their OWN true start dates.
        for a in ANCHORS:
            if i<indices[a]:
                continue
            b=acc[a]
            b["weighted"]+=z["tp"]*z["v"]
            b["vol"]+=z["v"]
            b["unweighted"]+=z["tp"]
            b["n"]+=1
        if i<indices["2023-07-27"]:
            continue
        def sma(n):
            if i+1<n:
                return None
            return sum(x["c"] for x in bars[i-n+1:i+1])/n
        w={a:acc[a]["weighted"]/acc[a]["vol"] for a in ANCHORS}
        b=acc["2023-07-27"]
        out.append({
            "date":z["date"],"close":z["c"],
            "avwap_author_anchor":w["2023-07-27"],
            "avwap_earlier_breakout":w["2023-05-25"],
            "avwap_local_low":w["2023-07-10"],
            "mean_hlc3_no_volume":b["unweighted"]/b["n"],
            "sma120_close":sma(120),"sma240_close":sma(240),
            "ema120_close":ema,"sessions_after_anchor":b["n"]
        })
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",type=Path,help="Local CSV (if missing, fetch pinned public GitHub source)")
    opt=p.parse_args()
    text=opt.csv.read_text(encoding="utf-8-sig") if opt.csv else urlopen(URL,timeout=15).read().decode("utf-8-sig")
    bars,excluded=read_bars(text)
    result=calculate(bars)
    assert len(bars)==756 and excluded==82 and len(result)==523
    check={r["date"]:r for r in result if r["date"] in CHECK}
    assert len(check)==len(CHECK)
    last=check["2025-09-18"]
    assert abs(last["avwap_author_anchor"]-184955.55525082286)<0.01
    assert abs(last["avwap_earlier_breakout"]-179544.3993385494)<0.01
    assert abs(last["avwap_local_low"]-183637.66803820754)<0.01
    assert abs(last["mean_hlc3_no_volume"]-184928.99936265138)<0.01
    assert abs(last["sma120_close"]-240964.16666666666)<0.01
    print(json.dumps({"input_valid_sessions":len(bars),"input_excluded":excluded,
                      "author_anchor_sessions":len(result),"checkpoints":check,
                      "decision":"NOT_IDENTIFIABLE; no exact matching original knee-price series",
                      "data_limit":"No bars past 2025-09-18 in source and volumes rounded"},
                     ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
