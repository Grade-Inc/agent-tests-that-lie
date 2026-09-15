from shop import apply_discount, line_total


def test_line_total_multiplies():
    assert line_total(499, 3) == 1497


def test_line_total_rejects_negative_quantity():
    try:
        line_total(499, -1)
    except ValueError:
        return
    raise AssertionError("a negative quantity should have been rejected")


def test_apply_discount_takes_the_percentage_off_the_whole_total():
    # 10% off $19.99 is $1.99 off, leaving $18.00.
    assert apply_discount(1999, 10) == 1800


def test_apply_discount_handles_the_edges():
    assert apply_discount(1999, 0) == 1999
    assert apply_discount(1999, 100) == 0
