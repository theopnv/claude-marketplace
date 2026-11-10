# shopcart

Price and shipping calculation for the checkout of our online shop. Used by the web store and the mobile app through the checkout API.

## Install and test

```
pip install -e .
pytest
```

## Business rules

### Discounts

- **R1.** Members of the loyalty program get 5% off the cart subtotal.
- **R2.** Carts with a subtotal of 100.00 or more get a 10% bulk discount.
- **R3.** Percentage discounts do not add up. When R1 and R2 both apply, the customer gets the higher one (10%).
- **R4.** A coupon takes a fixed amount off, after the percentage discount. Only one coupon per order. A coupon is valid only when the cart total after the percentage discount is at least 30.00.

Coupons: `SAVE10` (10.00 off), `WELCOME5` (5.00 off).

### Shipping

- **S1.** The parcel weight must be more than 0 kg and at most 30 kg. Other weights are rejected.
- **S2.** Fee by weight: up to 2 kg: 4.90. More than 2 kg up to 10 kg: 9.90. More than 10 kg up to 30 kg: 19.90.
- **S3.** Shipping is free when the cart total after discounts is 50.00 or more.

### Orders

- **O1.** Order states: NEW, PAID, SHIPPED, DELIVERED, CANCELLED.
- **O2.** Allowed changes: NEW to PAID (pay), NEW to CANCELLED (cancel), PAID to SHIPPED (ship), PAID to CANCELLED (cancel, the customer is refunded), SHIPPED to DELIVERED (deliver).
- **O3.** Any other event is rejected with `InvalidTransition` and the state does not change.

## FAQ for the support team

- *When is shipping free?* On orders over 50 €.
- *Can a customer use two coupons?* No, one coupon per order.
