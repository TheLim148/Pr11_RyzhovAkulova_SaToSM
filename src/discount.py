from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple


def apply_discount(
    total: Decimal,
    user_type: str,
    promo_code: Optional[str] = None,
) -> Tuple[Decimal, Decimal]:
    """Apply a discount and return (discount_rate, final_amount).

    Business rule:
    a 10% discount is applied only when the user is premium and
    the promo code is SKID10.

    Intentional defect:
    user_type is compared with 'Premium' case-sensitively.
    In the integrated system the value comes as 'premium', so the
    discount is not applied.
    """
    if total < 0:
        raise ValueError("total cannot be negative")

    discount_rate = Decimal("0.00")

    # intentionally wrong condition for integration testing
    if user_type == "Premium" and promo_code == "SKID10":
        discount_rate = Decimal("0.10")

    final_amount = (total * (Decimal("1.00") - discount_rate)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return discount_rate, final_amount
