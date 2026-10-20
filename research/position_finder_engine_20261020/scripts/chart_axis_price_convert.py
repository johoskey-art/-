"""Convert extracted band y-coordinates after an explicit linear/log axis audit.

No tick label is OCR'd or inferred.  Two reviewed tick anchors remain required
for each chart.  The axis scale in the calibration CSV determines interpolation.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def axis_price(y: float, y1: float, p1: float, y2: float, p2: float, scale: str) -> float:
    if y1 == y2:
        raise ValueError("axis calibration y positions must differ")
    if p1 <= 0 or p2 <= 0:
        raise ValueError("price tick anchors must be positive")
    fraction = (y - y1) / (y2 - y1)
    if scale == "linear":
        return p1 + fraction * (p2 - p1)
    if scale == "log":
        return math.exp(math.log(p1) + fraction * (math.log(p2) - math.log(p1)))
    raise ValueError("axis_scale must be linear or log")


def convert(observations_path: Path, calibration_path: Path, output_path: Path) -> tuple[int, int]:
    with calibration_path.open("r", encoding="utf-8-sig", newline="") as handle:
        calibrations = {row["image_id"]: row for row in csv.DictReader(handle)}
    with observations_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fieldnames = list(rows[0]) + ["axis_scale", "line_price", "conversion_status"]
    converted = skipped = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            calibration = calibrations.get(row["image_id"])
            if not calibration or calibration.get("calibration_status") != "READY":
                row.update(axis_scale="", line_price="", conversion_status="PENDING_CALIBRATION")
                skipped += 1
            else:
                try:
                    scale = calibration["axis_scale"]
                    price = axis_price(float(row["y_px"]), float(calibration["tick1_y_px"]), float(calibration["tick1_price"]), float(calibration["tick2_y_px"]), float(calibration["tick2_price"]), scale)
                except (KeyError, ValueError):
                    row.update(axis_scale=calibration.get("axis_scale", ""), line_price="", conversion_status="INVALID_CALIBRATION")
                    skipped += 1
                else:
                    row.update(axis_scale=scale, line_price=f"{price:.6f}", conversion_status="CONVERTED")
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
