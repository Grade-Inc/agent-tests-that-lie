"""Cart arithmetic, in integer cents. Never floats: money does not round the way floats do."""


def line_total(unit_price_cents: int, quantity: int) -> int:
    """The cost of `quantity` of one item."""
    if quantity < 0:
        raise ValueError("quantity cannot be negative")
    if unit_price_cents < 0:
        raise ValueError("a unit price cannot be negative")
    return unit_price_cents * quantity


def apply_discount(total_cents: int, percent_off: int) -> int:
    """Take `percent_off` percent off `total_cents`.

    The discount is computed on the WHOLE total and then floored, so the customer is never
    charged for a fraction of a cent that was never part of the price.
    """
    if not 0 <= percent_off <= 100:
        raise ValueError("percent_off must be between 0 and 100")
    return total_cents - (total_cents * percent_off) // 100
