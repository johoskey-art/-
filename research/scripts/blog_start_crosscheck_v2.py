#!/usr/bin/env python3
"""Reproduce the 009540/000660 blogger-start close vs high breakout audits.

Exploratory research only. Sources are pinned to a Git commit each.
The archive for 000660 begins 2022-08-18, so the 250/252-day
lookbacks on 2023-07-27 are NA (not inferred from 233 available sessions).
The archive's volumes are rounded to 0.01M; ratio is approximate.
The 009540 adjusted closing prices and raw highs are separate scales:
compare close-to-close or high-to-high, NEVER close-to-high.
"""
from __future__ import annotations
import argparse
import csv
import io
import re
import urllib.request
from pathlib import Path

HD_URL = ("https://raw.githubusercontent.com/choosunsick/Korea_Stocks/"
          "208a156b44db3a6be0fce4bb6280635d496d3369/"
          "Korea_Stocks_Full/009540.csv")
SK_URL = ("https://raw.githubusercontent.com/fnskcjswo123/Stock_AI/"
          "dcfecd1111c4262f9606706a728b75b28909b323/"
          "bin/sk%20%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4%20csv/"
          "000660%20%EA%B3%BC%EA%B1%B0%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%281%29.csv")
WINDOWS = (20, 60, 120, 240, 250, 252)
FIELDS = ["symbol", "date", "price_basis", "close", "high", "high_basis",
          "volume", "volume_precision", "prior_trading_days",
          "change_pct", "volume_to_prior20", "prior20_high_volume_mean"]
for n in WINDOWS:
    FIELDS += [f"prior_{n}_max_close", f"break_{n}_close",
               f"prior_{n}_max_high", f"break_{n}_high"]

def get_text(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8-sig")

def hd_rows(raw):
    rows = []
    for row in csv.DictReader(io.StringIO(raw)):
        try:
            rec = {"date": row["Date"], "close": float(row["Adj_Close"]),
                   "high": float(row["High"]), "volume": float(row["Volume"])}
            if rec["close"] > 0 and rec["volume"] > 0:
                rows.append(rec)
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(rows, key=lambda x: x["date"])

def sk_rows(raw):
    rows = []
    for row in csv.DictReader(io.StringIO(raw)):
        try:
            vol = row["거래량"].strip()
            mult = 1e6 if vol.endswith("M") else 1e3 if vol.endswith("K") else 1
            amount = float(vol.rstrip("MK")) * mult if vol else 0
            rec = {"date": re.sub(r"\s+", "", row["날짜"]),
                   "close": float(row["종가"].replace(",", "")),
                   "high": float(row["고가"].replace(",", "")),
                   "volume": amount}
            if rec["close"] > 0 and rec["volume"] > 0:
                rows.append(rec)
        except (KeyError, AttributeError, TypeError, ValueError):
            continue
    return sorted(rows, key=lambda x: x["date"])

def export(rows, symbol, start, end, close_basis, high_basis, precision, dest):
    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for i, r in enumerate(rows):
            if not start <= r["date"] <= end:
                continue
            prev20 = rows[i-20:i] if i >= 20 else []
            row = {
                "symbol": symbol, "date": r["date"], "price_basis": close_basis,
                "close": int(r["close"]), "high": int(r["high"]),
                "high_basis": high_basis, "volume": int(r["volume"]),
                "volume_precision": precision, "prior_trading_days": i,
                "change_pct": f"{100*(r['close']/rows[i-1]['close']-1):.9f}" if i else "",
                "volume_to_prior20": f"{r['volume']/(sum(p['volume'] for p in prev20)/20):.9f}" if prev20 else "",
                "prior20_high_volume_mean": f"{sum(p['volume'] for p in prev20)/20:.3f}" if prev20 else "",
            }
            for n in WINDOWS:
                if i >= n:
                    earlier = rows[i-n:i]
                    maxclose = max(p["close"] for p in earlier)
                    maxhigh = max(p["high"] for p in earlier)
                    row[f"prior_{n}_max_close"] = int(maxclose)
                    row[f"break_{n}_close"] = int(r["close"] > maxclose)
                    row[f"prior_{n}_max_high"] = int(maxhigh)
                    row[f"break_{n}_high"] = int(r["high"] > maxhigh)
                else:
                    row[f"prior_{n}_max_close"] = ""
                    row[f"break_{n}_close"] = ""
                    row[f"prior_{n}_max_high"] = ""
                    row[f"break_{n}_high"] = ""
            writer.writerow(row)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", type=Path,
                   default=Path(__file__).resolve().parents[1] / "results")
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    export(hd_rows(get_text(HD_URL)), "009540", "2004-12-20", "2005-01-21",
           "archival_Adj_Close", "archival_raw_High", "exact",
           args.output_dir / "009540_20050105_start_close_high_v2.csv")
    export(sk_rows(get_text(SK_URL)), "000660", "2023-07-03", "2023-08-04",
           "archival_Close", "archival_High", "rounded_0.01M",
           args.output_dir / "000660_20230727_start_close_high_v1.csv")
    print("Wrote the two start-day audit files; NA lookbacks are preserved.")

if __name__ == "__main__":
    main()
