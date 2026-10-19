#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch the original Samsung POP 141-firm SBT in CP949/CRLF format.
Usage: python patch_pop_141_alias_v5.py path/to/original_141.sbt
Requires original, unaltered 2026-10-19 141-firm SBT (either 6- or 17-group).
No network access. Does not modify the input file.
"""
from __future__ import annotations
import collections
import pathlib
import re
import sys


def parse(text: str):
    header = None
    sections = []
    current = None
    for line in text.splitlines():
        if line == "[GROUPINFO]":
            if header is not None:
                raise ValueError("duplicate GROUPINFO")
            header = {"name": line, "entries": [], "count": None}
            current = header
        elif re.fullmatch(r"\[\d{4}-.+\]", line):
            current = {"name": line, "entries": [], "count": None}
            sections.append(current)
        elif re.fullmatch(r"COUNT=\d+", line):
            current["count"] = int(line[6:])
        elif re.fullmatch(r"\d+=.*", line):
            current["entries"].append(line.split("=", 1)[1])
        elif line.strip():
            raise ValueError(f"Unexpected SBT line: {line[:80]!r}")
    if header is None or header["count"] != len(sections):
        raise ValueError("GROUPINFO count mismatch")
    for s in [header, *sections]:
        if s["count"] != len(s["entries"]):
            raise ValueError(f"Invalid COUNT in {s['name']}")
    return header, sections


def get_group(groups, index: int):
    expected = f"s. SEMI {index:02d} "
    found = [g for g in groups if expected in g["name"]]
    if len(found) != 1:
        raise ValueError(f"Expected exactly one SEMI {index:02d} group")
    return found[0]


def take_stock(g, stock_name: str):
    hits = [i for i, v in enumerate(g["entries"])
            if not v.startswith("@#") and v.split("@")[1] == stock_name]
    if len(hits) != 1:
        raise ValueError(f"Stock not unique in {g['name']}: {stock_name}")
    return g["entries"].pop(hits[0])


def find_header(g, subtitle: str):
    hits = [i for i, v in enumerate(g["entries"])
            if v.startswith("@#") and f"@@@{subtitle}@" in v]
    if len(hits) != 1:
        raise ValueError(f"Subtitle missing/duplicate in {g['name']}: {subtitle}")
    return hits[0]


def stock_positions(groups, name):
    return [g["name"] for g in groups for v in g["entries"]
            if not v.startswith("@#") and v.split("@")[1] == name]


def render(header, groups):
    lines = [header["name"], f"COUNT={len(groups)}"]
    lines.extend(f"{i}={v}" for i, v in enumerate(header["entries"]))
    for g in groups:
        lines += [g["name"], f"COUNT={len(g['entries'])}"]
        for i, value in enumerate(g["entries"]):
            if value.startswith("@#"):
                value = re.sub(r"^@#\d+", f"@#{i + 1}", value)
            lines.append(f"{i}={value}")
    return "\r\n".join(lines) + "\r\n"


def patch(input_path: pathlib.Path):
    raw = input_path.read_bytes()
    text = raw.decode("cp949")
    header, groups = parse(text)
    if len(groups) not in (6, 17):
        raise ValueError("Input must be 6-group or 17-group 141-firm SBT")
    semi = [g for g in groups if "s. SEMI " in g["name"]]
    if len(semi) != 6:
        raise ValueError("SEMI group count must be six")
    original_first_11 = [(g["name"], list(g["entries"])) for g in groups[:11]] if len(groups) == 17 else None

    before = [v for g in semi for v in g["entries"] if not v.startswith("@#")]
    if len(before) != 141 or len(set(v.split("@")[0] for v in before)) != 141:
        raise ValueError("Expected 141 unique stock records before editing")

    one, two, four = (get_group(groups, x) for x in (1, 2, 4))
    me = take_stock(one, "메카로")
    bc = take_stock(four, "비씨엔씨")
    np = take_stock(two, "뉴파워프라즈마")

    # Original F04-only RF heading becomes empty after moving Newpower.
    rf_idx = find_header(two, "RF 플라즈마 전원부품")
    if rf_idx + 1 < len(two["entries"]) and not two["entries"][rf_idx + 1].startswith("@#"):
        raise ValueError("RF subtitle has other stocks; do not delete blindly")
    two["entries"].pop(rf_idx)

    # F03 heater blocks and precursor delivery are separate sold products.
    idx = find_header(one, "전구체 공급 모듈")
    one["entries"][idx:idx] = ["@#1@@@증착용 히터블록@-1@@@1@-1@", me]

    # F04 synthetic quartz QD9/QD9+, not F10 common chamber parts.
    idx = find_header(two, "식각 가스·케미컬")
    two["entries"].insert(idx, bc)

    # Generator/matcher serves multiple processes; F10 common RF power.
    idx = find_header(four, "FOUP·퍼지·필터")
    four["entries"].insert(idx, np)

    if original_first_11 is not None:
        after11 = [(g["name"], g["entries"]) for g in groups[:11]]
        if after11 != original_first_11:
            raise ValueError("First 11 original groups changed unexpectedly")
    for stock in ("메카로", "비씨엔씨", "뉴파워프라즈마"):
        if len(stock_positions(semi, stock)) != 1:
            raise ValueError(f"{stock}: not exactly one SBT entry")
    if not ("SEMI 01" in stock_positions(semi, "메카로")[0]
            and "SEMI 02" in stock_positions(semi, "비씨엔씨")[0]
            and "SEMI 04" in stock_positions(semi, "뉴파워프라즈마")[0]):
        raise ValueError("Final company placements incorrect")

    out_text = render(header, groups)
    _, checked_groups = parse(out_text)
    allsemi = [g for g in checked_groups if "s. SEMI " in g["name"]]
    stocks = [v for g in allsemi for v in g["entries"] if not v.startswith("@#")]
    headings = set()
    for g in allsemi:
        for v in g["entries"]:
            if v.startswith("@#"):
                m = re.search(r"@@@([FB]\d\d) ", v)
                if m:
                    headings.add(m.group(1))
    needed = {f"F{i:02d}" for i in range(1, 11)} | {f"B{i:02d}" for i in range(1, 11)}
    if len(stocks) != 141 or len(set(v.split("@")[0] for v in stocks)) != 141:
        raise ValueError("Post-patch stock records corrupted")
    if headings != needed:
        raise ValueError(f"Process headings missing: {needed - headings}")

    out_path = input_path.with_name(input_path.stem + "_ALIAS_V5.sbt")
    if out_path.exists():
        raise FileExistsError(f"Refusing to overwrite {out_path}")
    data = out_text.encode("cp949")
    if data.count(b"\r\n") != len(out_text.splitlines()):
        raise ValueError("CRLF round-trip failed")
    out_path.write_bytes(data)
    print(f"OK {out_path} | groups={len(groups)} | SEMI_stocks=141 | processes=20 | bytes={len(data)} | CP949/CRLF")
    print("Original preserved. POP program import and overseas code validation still required.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python patch_pop_141_alias_v5.py original_141.sbt")
    patch(pathlib.Path(sys.argv[1]))
