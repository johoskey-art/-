from linear_axis_price_convert import linear_price


def test_linear_price() -> None:
    assert linear_price(150, 100, 1000, 200, 500) == 750


if __name__ == "__main__":
    test_linear_price()
    print("PASS")
