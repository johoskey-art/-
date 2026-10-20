"""Score predeclared normalized-band hypotheses against original chart q data.

This is a geometry test only.  A surviving candidate is not the blogger's
unpublished generating formula.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

BANDS = ("shoulder_q_from_top", "waist_q_from_top", "thigh_q_from_top")
CANDIDATES = {
    "q_1_5__2_5__5_7": (1 / 5, 2 / 5, 5 / 7),
    "q_1_5__3_7__5_7": (1 / 5, 3 / 7, 5 / 7),
    "canonical_fibonacci_0_236__0_382__0_618": (0.236068, 0.381966, 0.618034),
}


def losses(rows: list[dict[str, str]], q: tuple[float, float, float]) -> dict[str, float]:
    errors = [abs(float(row[band]) - q[index]) for row in rows for index, band in enumerate(BANDS)]
    return {
        "mae": sum(errors) / len(errors),
        "rmse": (sum(error * error for error in errors) / len(errors)) ** 0.5,
        "max_abs_error": max(errors),
    }


def analyze(input_path: Path) -> dict[str, object]:
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["original_price_axis"] == "LOG"]
    if not rows:
        raise ValueError("no LOG rows")
    observed_mean = tuple(sum(float(row[band]) for row in rows) / len(rows) for band in BANDS)
    candidates = dict(CANDIDATES)
    candidates["sample_mean_not_a_formula"] = observed_mean
    return {
        "n_log_screens": len(rows),
        "bands": BANDS,
        "observed_mean_q": observed_mean,
        "scores": {name: {"q": q, **losses(rows, q)} for name, q in candidates.items()},
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = analyze(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
