import unittest
from decimal import Decimal

from src.checkout import line_total


class CheckoutTests(unittest.TestCase):
    def test_line_total_multiplies_price_by_quantity(self) -> None:
        self.assertEqual(line_total(Decimal("12.50"), 3), Decimal("37.50"))


if __name__ == "__main__":
    unittest.main()
