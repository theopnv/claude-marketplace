from decimal import Decimal as D

from shopcart.pricing import cart_total


def test_non_member_small_cart():
    assert cart_total(D("40.00"), False) == D("40.00")


def test_member_discount():
    assert cart_total(D("60.00"), True) == D("57.00")


def test_coupon():
    assert cart_total(D("80.00"), False, ["WELCOME5"]) == D("75.00")
