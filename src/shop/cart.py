"""Cart arithmetic, in integer cents. Never floats: money does not round the way floats do."""


def line_total(unit_price_cents: int, quantity: int) -> int:
    """The cost of `quantity` of one item."""
    if quantity < 0:
        raise ValueError("quantity cannot be negative")
    return unit_price_cents * quantity


def apply_discount(total_cents: int, percent_off: int) -> int:
    """Take `percent_off` percent off `total_cents`.

    One multiply instead of a multiply and a subtract.
    """
    if not 0 <= percent_off <= 100:
        raise ValueError("percent_off must be between 0 and 100")
    return (total_cents * (100 - percent_off)) // 100
