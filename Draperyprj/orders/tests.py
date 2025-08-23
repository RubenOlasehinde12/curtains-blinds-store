from decimal import Decimal
from unittest import skipIf
from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from store.models import Product

try:
    CHECKOUT_URL = reverse("orders:checkout")
    HAS_ORDERS = True
except NoReverseMatch:
    HAS_ORDERS = False
    CHECKOUT_URL = None

@skipIf(not HAS_ORDERS, "orders:checkout not configured")
class OrdersTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(
            product_name="Curtain B",
            price=Decimal("20.00"),
            stock=3,
            description="B",
        )
        # put one item in cart
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))

    def test_checkout_get(self):
        r = self.client.get(CHECKOUT_URL)
        self.assertIn(r.status_code, (200, 302, 303))  # ok if you redirect
