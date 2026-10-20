from mixed_stage_layout_candidates import bands_from_anchors


def test_candidate_a_is_ordered_and_uses_log_stages() -> None:
    bands = bands_from_anchors(100, 1000, "MIXED_5_7_A")
    assert bands["knee"] < bands["thigh"] < bands["waist"] < bands["shoulder"] < bands["top"]
    assert round(bands["thigh"], 6) == round(100 * (10 ** (2 / 7)), 6)


if __name__ == "__main__":
    test_candidate_a_is_ordered_and_uses_log_stages()
    print("PASS")
