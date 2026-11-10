from decimal import Decimal

from .pricing import cart_total
from .shipping import shipping_fee


def checkout(subtotal: Decimal, is_member: bool, weight_kg: Decimal, coupon_codes=()) -> dict:
    total = cart_total(subtotal, is_member, coupon_codes)
    fee = shipping_fee(weight_kg, total)
    return {"items_total": total, "shipping": fee, "grand_total": total + fee}
