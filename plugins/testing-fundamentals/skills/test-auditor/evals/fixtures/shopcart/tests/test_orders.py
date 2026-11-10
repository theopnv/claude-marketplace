from shopcart.orders import Order


def test_happy_path():
    order = Order("A-1001")
    order.handle("pay")
    order.handle("ship")
    order.handle("deliver")
    assert order.state == "DELIVERED"
