from dataclasses import dataclass
from decimal import Decimal


PAYMENT_LIMIT = Decimal("10000.00")


@dataclass(frozen=True)
class PaymentResult:
    status: str
    message: str


def process_payment(amount: Decimal) -> PaymentResult:
    """Process the payment.

    The demo system does not connect to a real payment provider.
    It only checks a business limit.
    """
    if amount < 0:
        return PaymentResult("failed", "payment amount cannot be negative")

    if amount <= PAYMENT_LIMIT:
        return PaymentResult("success", "payment accepted")

    return PaymentResult("failed", "payment limit exceeded")
