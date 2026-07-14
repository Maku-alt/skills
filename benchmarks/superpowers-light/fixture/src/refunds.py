from decimal import Decimal


def issue_refund(
    captured: Decimal,
    already_refunded: Decimal,
    requested: Decimal,
) -> Decimal:
    if requested <= 0:
        raise ValueError("refund must be positive")
    if requested > captured:
        raise ValueError("refund exceeds captured amount")
    return already_refunded + requested
