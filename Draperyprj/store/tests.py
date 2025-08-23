from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from store.models import Product

class StoreTests(TestCase):
    def setUp(self):
        self.p = Product.objects.create(
            product_name="Curtain A",
            price=Decimal("28.99"),
            stock=10,
            description="Test item",
        )

    def test_list(self):
        r = self.client.get(reverse("store:product_list"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Curtain A")

    def test_detail(self):
        r = self.client.get(reverse("store:product_detail", args=[self.p.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "€28.99")

    def test_search(self):
        r = self.client.get(reverse("store:search_results"), {"q": "Curtain"})
        self.assertEqual(r.status_code, 200)

    def test_contact_about(self):
        self.assertEqual(self.client.get(reverse("store:contact")).status_code, 200)
        self.assertEqual(self.client.get(reverse("store:about")).status_code, 200)
