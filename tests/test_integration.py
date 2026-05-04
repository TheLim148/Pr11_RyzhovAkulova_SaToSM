# ------------------------------------------------------------
# file: tests/test_integration.py
# practical work 11: integration testing
#
# These tests intentionally include expected business behavior.
# Two tests fail because of the integration defect between the
# integration layer and module B.
# ------------------------------------------------------------

from decimal import Decimal
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.cart import CartItem
from src.discount import apply_discount
from src.order_service import create_order
from src.payment import process_payment


def item(name: str, price: str, quantity: int) -> CartItem:
    return CartItem(name=name, price=Decimal(price), quantity=quantity)


class TestShopIntegration(unittest.TestCase):
    def test_01_regular_user_without_promo_success(self):
        result = create_order(
            items=[item("keyboard", "1000.00", 1)],
            user_type="regular",
            promo_code=None,
        )

        self.assertEqual(result["total"], Decimal("1000.00"))
        self.assertEqual(result["discount_rate"], Decimal("0.00"))
        self.assertEqual(result["final_amount"], Decimal("1000.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_02_premium_user_with_promo_gets_discount(self):
        result = create_order(
            items=[item("monitor", "5000.00", 1)],
            user_type="premium",
            promo_code="SKID10",
        )

        self.assertEqual(result["discount_rate"], Decimal("0.10"))
        self.assertEqual(result["final_amount"], Decimal("4500.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_03_premium_order_should_be_below_limit_after_discount(self):
        result = create_order(
            items=[item("laptop", "10000.00", 1)],
            user_type="premium",
            promo_code="SKID10",
        )

        self.assertEqual(result["discount_rate"], Decimal("0.10"))
        self.assertEqual(result["final_amount"], Decimal("9000.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_04_regular_user_with_promo_has_no_premium_discount(self):
        result = create_order(
            items=[item("chair", "5000.00", 1)],
            user_type="regular",
            promo_code="SKID10",
        )

        self.assertEqual(result["discount_rate"], Decimal("0.00"))
        self.assertEqual(result["final_amount"], Decimal("5000.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_05_module_b_to_c_direct_premium_discount_success(self):
        discount_rate, final_amount = apply_discount(
            total=Decimal("5000.00"),
            user_type="Premium",
            promo_code="SKID10",
        )
        payment = process_payment(final_amount)

        self.assertEqual(discount_rate, Decimal("0.10"))
        self.assertEqual(final_amount, Decimal("4500.00"))
        self.assertEqual(payment.status, "success")

    def test_06_module_b_to_c_direct_premium_discount_still_over_limit(self):
        discount_rate, final_amount = apply_discount(
            total=Decimal("12000.00"),
            user_type="Premium",
            promo_code="SKID10",
        )
        payment = process_payment(final_amount)

        self.assertEqual(discount_rate, Decimal("0.10"))
        self.assertEqual(final_amount, Decimal("10800.00"))
        self.assertEqual(payment.status, "failed")

    def test_07_empty_cart_can_be_processed(self):
        result = create_order(
            items=[],
            user_type="regular",
            promo_code=None,
        )

        self.assertEqual(result["total"], Decimal("0.00"))
        self.assertEqual(result["final_amount"], Decimal("0.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_08_boundary_payment_limit_success(self):
        result = create_order(
            items=[item("server", "10000.00", 1)],
            user_type="regular",
            promo_code=None,
        )

        self.assertEqual(result["final_amount"], Decimal("10000.00"))
        self.assertEqual(result["payment_status"], "success")

    def test_09_payment_limit_exceeded(self):
        result = create_order(
            items=[item("server", "10000.01", 1)],
            user_type="regular",
            promo_code=None,
        )

        self.assertEqual(result["final_amount"], Decimal("10000.01"))
        self.assertEqual(result["payment_status"], "failed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
