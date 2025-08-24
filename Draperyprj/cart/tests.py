from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from store.models import Product
from cart.models import CartItem

class CartTests(TestCase):
    def setUp(self):
        
        self.client.get(reverse("cart:cart_detail"))
        self.p = Product.objects.create(
            product_name="Curtain A",
            price=Decimal("12.50"),
            stock=5,
            description="A",
        )

    def test_add_and_view(self):
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))
        r = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Curtain A")

    def test_decrement_and_remove(self):
       
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))
   
        self.client.get(reverse("cart:decrement_cart", args=[self.p.pk]))
      
        self.client.get(reverse("cart:decrement_cart", args=[self.p.pk]))
        self.assertFalse(CartItem.objects.filter(product=self.p).exists())

    def test_clear(self):
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))
        self.client.get(reverse("cart:clear_cart"))
        self.assertEqual(CartItem.objects.count(), 0)

    def test_basket_page(self):
        self.client.get(reverse("cart:add_cart", args=[self.p.pk]))
        r = self.client.get(reverse("cart:basket"))
        self.assertEqual(r.status_code, 200)
