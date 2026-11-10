from decimal import Decimal

from .coupons import apply_coupons
from .money import money

MEMBER_RATE = Decimal("0.05")
BULK_RATE = Decimal("0.10")
BULK_THRESHOLD = Decimal("100.00")


def percentage_discount(subtotal: Decimal, is_member: bool) -> Decimal:
    rate = Decimal("0")
    if is_member:
        rate += MEMBER_RATE
    if subtotal >= BULK_THRESHOLD:
        rate += BULK_RATE
    return money(subtotal * rate)


def cart_total(subtotal: Decimal, is_member: bool, coupon_codes=()) -> Decimal:
    discounted = subtotal - percentage_discount(subtotal, is_member)
    discounted -= apply_coupons(subtotal, coupon_codes)
    return money(max(discounted, Decimal("0")))
