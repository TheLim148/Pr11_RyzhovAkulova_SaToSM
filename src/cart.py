from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


@dataclass(frozen=True)
class CartItem:
    name: str
    price: Decimal
    quantity: int


def calculate_total(items: Iterable[CartItem]) -> Decimal:
    """Calculate the total cart amount.

    Raises:
        ValueError: if item price or quantity is invalid.
    """
    total = Decimal("0.00")

    for item in items:
        if item.price < 0:
            raise ValueError(f"price cannot be negative: {item.name}")
        if item.quantity < 0:
            raise ValueError(f"quantity cannot be negative: {item.name}")

        total += item.price * item.quantity

    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
