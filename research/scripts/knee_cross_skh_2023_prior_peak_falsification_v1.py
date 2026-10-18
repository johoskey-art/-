#!/usr/bin/env python3
"""Knee-cross vs prior MAJOR cycle peak: SK Hynix 2021-2023 counterexample.

Code computes only observable highs from two GitHub-pinned historical archives.
It NEVER asserts that 2023-07-27 is the exact knee crossing, because the blogger
only stated 'knee crossed in 2023' in blog_content.txt.
The 2021 archived source ends 2021-04-16: 2021 values are KNOWN LOWER
BOUNDS on maxima, not claims of a full 2021 database.
2023 archive includes 245 valid session bars: every 2023 daily record.
"""
from __future__ import annotations
import argparse
import csv
import io
import urllib.request
from pathlib import Path

OLD_URL = ("https://raw.githubusercontent.com/choosunsick/Korea_Stocks/"
           "208a156b44db3a6be0fce4bb6280635d496d3369/"
           "Korea_Stocks_Full/000660.csv")
NEW_URL = ("https://raw.githubusercontent.com/fnskcjswo123/Stock_AI/"
           "dcfecd1111c4262f9606706a728b75b28909b323/"
           "bin/sk%20%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4%20csv/"
           "000660%20%EA%B3%BC%EA%B1%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%281%29.csv")

def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as h:
        return h.read().decode("utf-8-sig")

def load_old(s: str):
    for r in csv.DictReader(io.StringIO(s)):
        try:
            d = r["Date"]
            c, h, v = (float(r["Close"]), float(r["High"]), float(r["Volume"]))
            if v > 0 and c > 0 and h > 0:
                yield {"date": d, "close": c, "high": h}
        except (KeyError, ValueError, TypeError):
            pass

def load_new(s: str):
    for r in csv.DictReader(io.StringIO(s)):
        try:
            d = "".join(r["날짜"].split())
            c = float(r["종가"].replace(",", ""))
            h = float(r["고가"].replace(",", ""))
            if r["거래량"] and c > 0 and h > 0:
                yield {"date": d, "close": c, "high": h}
        except (KeyError, ValueError, TypeError, AttributeError):
            pass

def verify(old, new):
    a = [r for r in old if r["date"].startswith("2021")]
    b = [r for r in new if r["date"].startswith("2023")]
    assert len(a) >= 50 and len(b) >= 240, "incomplete or malformed source: refuse"
    ac = max(a, key=lambda r: r["close"])
    ah = max(a, key=lambda r: r["high"])
    bc = max(b, key=lambda r: r["close"])
    bh = max(b, key=lambda r: r["high"])
    assert ac["close"] > bc["close"], "the no-recovery conclusion fails"
    assert ah["high"] > bh["high"], "the no-recovery conclusion fails"
    return {
        "known_2021_close_lower_bound": ac,
        "known_2021_intraday_high_lower_bound": ah,
        "all_2023_max_close": bc,
        "all_2023_max_high": bh,
        "source_2021_trading_rows_available": len(a),
        "source_2023_trading_rows_available": len(b),
        "2023_high_below_known_2021_high_pct": round(100*(bh["high"]/ah["high"]-1), 6),
        "2023_close_below_known_2021_close_pct": round(100*(bc["close"]/ac["close"]-1), 6),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-local", type=Path)
    parser.add_argument("--new-local", type=Path)
    args = parser.parse_args()
    old_text = args.old_local.read_text(encoding="utf-8-sig") if args.old_local else fetch(OLD_URL)
    new_text = args.new_local.read_text(encoding="utf-8-sig") if args.new_local else fetch(NEW_URL)
    import json
    print(json.dumps(verify(list(load_old(old_text)), list(load_new(new_text))),
                     indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
