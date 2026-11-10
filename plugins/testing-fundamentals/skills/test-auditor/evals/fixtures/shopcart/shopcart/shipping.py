from decimal import Decimal

FREE_SHIPPING_THRESHOLD = Decimal("50.00")
MAX_WEIGHT = Decimal("30")


def shipping_fee(weight_kg: Decimal, order_total: Decimal) -> Decimal:
    if weight_kg <= 0 or weight_kg > MAX_WEIGHT:
        raise ValueError("weight out of range")
    if order_total > FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    if weight_kg <= 2:
        return Decimal("4.90")
    if weight_kg < 10:
        return Decimal("9.90")
    return Decimal("19.90")
