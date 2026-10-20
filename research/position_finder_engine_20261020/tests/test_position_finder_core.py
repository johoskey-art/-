from position_finder_core import classify_price, historical_stage_references, named_layout_ranges


def test_historical_reference_prices() -> None:
    rows = [
        {"k": 5, "j": 0, "stage_ratio_p25": 1, "stage_ratio_median": 1, "stage_ratio_p75": 1},
        {"k": 5, "j": 1, "stage_ratio_p25": 1.4, "stage_ratio_median": 1.5, "stage_ratio_p75": 1.6},
    ]
    result = historical_stage_references(rows, cycle_low=100, k=5)
    assert [(item.low, item.median, item.high) for item in result] == [(100, 100, 100), (140, 150, 160)]


def test_named_band_ranges_and_classification() -> None:
    bands = named_layout_ranges(
        knee_price=100,
        top_price=1000,
        q_ranges={
            "shoulder": (0.206, 0.224, 0.242),
            "waist": (0.412, 0.438, 0.465),
            "thigh": (0.713, 0.736, 0.760),
        },
    )
    assert all(item.low <= item.median <= item.high for item in bands)
    assert classify_price(300, bands) == "thigh_to_waist"


if __name__ == "__main__":
    test_historical_reference_prices()
    test_named_band_ranges_and_classification()
    print("PASS")

