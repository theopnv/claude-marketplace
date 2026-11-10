# Issue #87: Shipping charged on a 50.00 order

Reported by support, 2026-10-28.

A customer paid 50.00 for items and was charged 9.90 shipping. Our FAQ says shipping is free on orders over 50 €, but the business rules (README, S3) say 50.00 or more is free. The product owner confirmed that S3 is correct.

Steps: non-member, subtotal 50.00, no coupon, parcel 5 kg. Expected shipping 0.00, actual 9.90.
