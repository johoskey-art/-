from screen_q_candidate_test import losses


def test_candidate_loss_is_zero_for_exact_rows() -> None:
    rows = [{"shoulder_q_from_top": "0.2", "waist_q_from_top": "0.4", "thigh_q_from_top": str(5 / 7)}]
    output = losses(rows, (0.2, 0.4, 5 / 7))
    assert output["mae"] == 0
    assert output["rmse"] == 0


if __name__ == "__main__":
    test_candidate_loss_is_zero_for_exact_rows()
    print("PASS")
