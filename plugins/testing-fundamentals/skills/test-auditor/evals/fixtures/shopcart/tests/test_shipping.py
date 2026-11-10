from decimal import Decimal as D

from shopcart.shipping import shipping_fee


def test_medium_parcel():
    assert shipping_fee(D("5"), D("20.00")) == D("9.90")


def test_free_shipping():
    assert shipping_fee(D("5"), D("80.00")) == D("0.00")


def test_heavy_parcel():
    shipping_fee(D("25"), D("20.00"))
