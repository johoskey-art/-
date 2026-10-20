from axis_price_convert import axis_price


def test_log_axis_price() -> None:
    assert round(axis_price(150, 100, 1000, 200, 100, "log"), 6) == round(1000 * (0.1 ** 0.5), 6)


def test_linear_axis_price() -> None:
    assert axis_price(150, 100, 1000, 200, 500, "linear") == 750


if __name__ == "__main__":
    test_log_axis_price()
    test_linear_axis_price()
    print("PASS")
