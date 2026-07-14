from decimal import Decimal


def line_total(unit_price: Decimal, quantity: int) -> Decimal:
    """Return the total for one checkout line."""
    return unit_price * quantity
