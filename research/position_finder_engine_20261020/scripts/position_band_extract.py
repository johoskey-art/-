"""Draft extractor for colored price-position bands in locally stored HTS screenshots.

This script never treats a screen-pixel measurement as an exact original indicator
value.  It writes one row per screen-x sample and band, with a review flag.
Raw screenshots stay outside the repository; only CSV observations are exportable.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np


CHART_SORT_INDICES = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 14, 16, 18, 21, 24, 27, 30,
    32, 33, 34, 35, 36, 37, 38, 41,
}


def sorted_screenshots(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.png"), key=lambda p: p.stat().st_mtime)


def color_masks(image_bgr: np.ndarray) -> dict[str, np.ndarray]:
    """Broad masks; later visual review decides whether a segment is a true band."""
    b, g, r = cv2.split(image_bgr)
    masks = {
        "top": (r > 175) & (g < 125) & (b < 125),
        "shoulder": (g > 105) & (r < 150) & (b < 155),
        "thigh": (r > 175) & (g > 45) & (g < 205) & (b < 115),
        "knee": (b > 115) & (r < 145) & (g < 175),
        "waist": (r < 88) & (g < 88) & (b < 88),
    }
    return {name: mask.astype(np.uint8) for name, mask in masks.items()}


def y_candidates(mask: np.ndarray, x: int, half_width: int, y0: int, y1: int) -> list[int]:
    x0 = max(0, x - half_width)
    x1 = min(mask.shape[1], x + half_width + 1)
    local = mask[y0:y1, x0:x1]
    rows = np.where(local.sum(axis=1) > 0)[0]
    if rows.size == 0:
        return []
    # Merge immediately adjacent painted rows into one candidate centre.
    groups: list[list[int]] = [[int(rows[0])]]
    for row in rows[1:]:
        if int(row) <= groups[-1][-1] + 2:
            groups[-1].append(int(row))
        else:
            groups.append([int(row)])
    return [int(round(y0 + np.median(group))) for group in groups]


def choose_ordered(candidates: dict[str, list[int]], y0: int, y1: int) -> dict[str, int | None]:
    """Choose a monotonic top��shoulder��waist��thigh��knee sequence.

    The function deliberately returns None rather than forcing a match when a
    coloured text label, candlestick, or hidden line makes the order impossible.
    """
    order = ["top", "shoulder", "waist", "thigh", "knee"]
    chosen: dict[str, int | None] = {band: None for band in order}
    previous = y0 - 1
    for band in order:
        pool = [y for y in candidates[band] if y > previous + 2]
        if not pool:
            continue
        # Position bands normally occupy a broad vertical span. Choose the
        # first ordered colour trace; label/text artefacts are reviewed later.
        selected = min(pool)
        chosen[band] = selected
        previous = selected
    if chosen["top"] is not None and chosen["knee"] is not None:
        if chosen["knee"] - chosen["top"] < max(18, int((y1 - y0) * 0.06)):
            return {band: None for band in order}
    return chosen


def samples_for_image(path: Path, image_id: str, local_index: int) -> Iterable[dict[str, object]]:
    # cv2.imread cannot reliably open Korean Windows paths in this runtime.
    encoded = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image is None:
        return []
    height, width = image.shape[:2]
    # HTS plot region excluding toolbar, lower oscillators, left/right price labels.
    y0, y1 = int(height * 0.13), int(height * 0.72)
    x0, x1 = int(width * 0.09), int(width * 0.88)
    masks = color_masks(image)
    rows: list[dict[str, object]] = []
    for fraction in (0.20, 0.50, 0.80):
        x = int(x0 + (x1 - x0) * fraction)
        candidates = {band: y_candidates(mask, x, 4, y0, y1) for band, mask in masks.items()}
        chosen = choose_ordered(candidates, y0, y1)
        top, knee = chosen["top"], chosen["knee"]
        span = (knee - top) if top is not None and knee is not None else None
        for band, y in chosen.items():
            q = None
            if span and y is not None and span > 0:
                q = (y - top) / span
            quality = "AUTO_DRAFT"
            if y is None:
                quality = "NOT_FOUND"
            rows.append(
                {
                    "image_id": image_id,
                    "local_sort_index": local_index,
                    "source_file_name": path.name,
                    "x_fraction": f"{fraction:.2f}",
                    "x_px": x,
                    "band": band,
                    "y_px": "" if y is None else y,
                    "screen_q_top_to_knee": "" if q is None else f"{q:.6f}",
                    "plot_y0": y0,
                    "plot_y1": y1,
                    "price_axis": "UNKNOWN",
                    "observation_quality": quality,
                    "review_required": "YES",
                    "method": "broad_rgb_mask_ordered_sequence_v0",
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    for index, path in enumerate(sorted_screenshots(args.input_dir)):
        if index not in CHART_SORT_INDICES:
            continue
        rows.extend(samples_for_image(path, f"PF{index:03d}", index))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "image_id", "local_sort_index", "source_file_name", "x_fraction", "x_px",
        "band", "y_px", "screen_q_top_to_knee", "plot_y0", "plot_y1", "price_axis",
        "observation_quality", "review_required", "method",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary_rows = []
    for image_id in sorted({str(row["image_id"]) for row in rows}):
        image_rows = [row for row in rows if row["image_id"] == image_id]
        by_band = {
            band: [float(row["screen_q_top_to_knee"]) for row in image_rows if row["band"] == band and row["screen_q_top_to_knee"] != ""]
            for band in ("shoulder", "waist", "thigh")
        }
        missing = sum(1 for row in image_rows if row["observation_quality"] == "NOT_FOUND")
        stats = {}
        for band, values in by_band.items():
            stats[f"{band}_q_mean"] = "" if not values else f"{np.mean(values):.6f}"
            stats[f"{band}_q_std"] = "" if len(values) < 2 else f"{np.std(values):.6f}"
        quality = "AUTO_REVIEW"
        if missing:
            quality = "INCOMPLETE"
        elif any(len(values) != 3 for values in by_band.values()):
            quality = "INCOMPLETE"
        summary_rows.append(
            {
                "image_id": image_id,
                "local_sort_index": image_rows[0]["local_sort_index"],
                "total_observations": len(image_rows),
                "not_found": missing,
                "review_status": quality,
                **stats,
            }
        )
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_output.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "image_id", "local_sort_index", "total_observations", "not_found", "review_status",
            "shoulder_q_mean", "shoulder_q_std", "waist_q_mean", "waist_q_std", "thigh_q_mean", "thigh_q_std",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"wrote {len(rows)} observations to {args.output}")
    print(f"wrote {len(summary_rows)} image summaries to {args.summary_output}")


if __name__ == "__main__":
    main()

