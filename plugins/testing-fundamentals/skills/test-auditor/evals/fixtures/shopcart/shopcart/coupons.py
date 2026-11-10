from decimal import Decimal

COUPONS = {"SAVE10": Decimal("10.00"), "WELCOME5": Decimal("5.00")}
MIN_CART = Decimal("30.00")


class UnknownCoupon(ValueError):
    pass


def apply_coupons(cart_amount: Decimal, codes) -> Decimal:
    """Return the total reduction that the coupons give on this cart."""
    if cart_amount < MIN_CART:
        return Decimal("0")
    total = Decimal("0")
    for code in codes:
        if code not in COUPONS:
            raise UnknownCoupon(code)
        total += COUPONS[code]
    return total
