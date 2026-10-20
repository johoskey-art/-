"""Convert auto-extracted line y-coordinates using manually audited price ticks.

This script is deliberately narrow: it never OCRs or guesses a price-axis
number. A reviewer supplies two visible tick anchors for a chart and the
script transforms the already-recorded line pixels on a verified linear axis.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def linear_price(y_px: float, y1_px: float, price1: float, y2_px: float, price2: float) -> float:
    """Map a screen y-coordinate to price using two known linear-axis ticks."""
    if y1_px == y2_px:
        raise ValueError("axis calibration y positions must differ")
    return price1 + (y_px - y1_px) * (price2 - price1) / (y2_px - y1_px)


def read_calibrations(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["image_id"]: row for row in csv.DictReader(handle)}


def convert(observations_path: Path, calibration_path: Path, output_path: Path) -> tuple[int, int]:
    calibrations = read_calibrations(calibration_path)
    converted = 0
    skipped = 0
    with observations_path.open("r", encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
        fieldnames = list(rows[0].keys()) + ["axis_scale", "line_price", "conversion_status"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            calibration = calibrations.get(row["image_id"])
            if not calibration or calibration.get("calibration_status") != "READY" or calibration.get("axis_scale") != "linear":
                row.update(axis_scale="", line_price="", conversion_status="PENDING_CALIBRATION")
                skipped += 1
            else:
                try:
                    price = linear_price(float(row["y_px"]), float(calibration["tick1_y_px"]), float(calibration["tick1_price"]), float(calibration["tick2_y_px"]), float(calibration["tick2_price"]))
                except (KeyError, ValueError):
                    row.update(axis_scale="linear", line_price="", conversion_status="INVALID_CALIBRATION")
                    skipped += 1
                else:
                    row.update(axis_scale="linear", line_price=f"{price:.6f}", conversion_status="CONVERTED")
                    converted += 1
            writer.writerow(row)
    return converted, skipped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--calibrations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    converted, skipped = convert(args.observations, args.calibrations, args.output)
    print(f"converted={converted} skipped={skipped}")


if __name__ == "__main__":
    main()
