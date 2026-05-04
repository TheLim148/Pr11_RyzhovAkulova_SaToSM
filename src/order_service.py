from decimal import Decimal
from typing import Iterable, Optional, TypedDict

from .cart import CartItem, calculate_total
from .discount import apply_discount
from .payment import process_payment


class OrderResult(TypedDict):
    total: Decimal
    discount_rate: Decimal
    final_amount: Decimal
    payment_status: str
    payment_message: str


def create_order(
    items: Iterable[CartItem],
    user_type: str,
    promo_code: Optional[str] = None,
) -> OrderResult:
    """Create an order using modules A, B and C.

    Integration data flow:
    module A -> total amount;
    module B -> discount rate and final amount;
    module C -> payment status.
    """
    total = calculate_total(items)

    # The integration layer normalizes user input.
    # Because module B expects "Premium" exactly, this lowercase value
    # demonstrates a defect on the boundary between modules.
    normalized_user_type = user_type.strip().lower()

    discount_rate, final_amount = apply_discount(
        total=total,
        user_type=normalized_user_type,
        promo_code=promo_code,
    )

    payment_result = process_payment(final_amount)

    return {
        "total": total,
        "discount_rate": discount_rate,
        "final_amount": final_amount,
        "payment_status": payment_result.status,
        "payment_message": payment_result.message,
    }
