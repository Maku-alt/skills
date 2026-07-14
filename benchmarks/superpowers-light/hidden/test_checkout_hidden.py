import unittest
from decimal import Decimal

from src.checkout import line_total


class CheckoutHiddenTests(unittest.TestCase):
    def test_negative_quantity_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            line_total(Decimal("10.00"), -1)


if __name__ == "__main__":
    unittest.main()
