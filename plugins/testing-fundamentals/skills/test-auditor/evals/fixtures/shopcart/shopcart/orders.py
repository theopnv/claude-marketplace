class InvalidTransition(Exception):
    pass


_TRANSITIONS = {
    ("NEW", "pay"): "PAID",
    ("NEW", "cancel"): "CANCELLED",
    ("PAID", "ship"): "SHIPPED",
    ("PAID", "cancel"): "CANCELLED",
    ("SHIPPED", "deliver"): "DELIVERED",
    ("SHIPPED", "cancel"): "CANCELLED",
}


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.state = "NEW"
        self.refunded = False

    def handle(self, event: str) -> str:
        key = (self.state, event)
        if key not in _TRANSITIONS:
            raise InvalidTransition(f"{event} is not allowed in state {self.state}")
        if event == "cancel" and self.state == "PAID":
            self.refunded = True
        self.state = _TRANSITIONS[key]
        return self.state
