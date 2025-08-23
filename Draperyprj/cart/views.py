# cart/views.py
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from store.models import Product
from .models import Cart, CartItem  # <- import Cart (FK) and CartItem

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def _session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _get_cart(request):
    sk = _session_key(request)
    cart, _ = Cart.objects.get_or_create(cart_id=sk)  # your Cart has cart_id (string)
    return cart


def _to_cents(amount) -> int:
    if amount is None:
        return 0
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def add_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={"quantity": 1, "active": True},
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart:cart_detail")


def decrement_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    try:
        item = CartItem.objects.get(product=product, cart=cart)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect("cart:cart_detail")


def remove_cart_item(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    CartItem.objects.filter(product=product, cart=cart).delete()
    return redirect("cart:cart_detail")


def clear_cart(request):
    cart = _get_cart(request)
    CartItem.objects.filter(cart=cart).delete()
    messages.info(request, "Cart cleared.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = _get_cart(request)

    cart_items = list(
        CartItem.objects.filter(cart=cart).select_related("product")
    )
    total = Decimal("0")
    for ci in cart_items:
        ci.sub_total = ci.product.price * ci.quantity
        total += ci.sub_total

    counter = sum(ci.quantity for ci in cart_items)

    if request.method == "POST":
        stripe_total = _to_cents(total)
        if stripe_total <= 0:
            return render(request, "cart/cart.html", {
                "cart_items": cart_items, "total": total, "counter": counter,
                "error": "Cart total must be greater than 0.",
            })
        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": "Cart total"},
                        "unit_amount": stripe_total,
                    },
                    "quantity": 1,
                }],
                payment_intent_data={"description": "Online Shop - New Order"},
                success_url=request.build_absolute_uri(reverse("store:product_list")),
                cancel_url=request.build_absolute_uri(reverse("cart:cart_detail")),
            )
            return redirect(session.url, code=303)
        except Exception as e:
            return render(request, "cart/cart.html", {
                "cart_items": cart_items, "total": total, "counter": counter,
                "error": str(e),
            })

    return render(request, "cart/cart.html", {
        "cart_items": cart_items, "total": total, "counter": counter,
    })


def basket(request):
    cart = _get_cart(request)
    items = list(
        CartItem.objects.filter(cart=cart).select_related("product")
    )

    total = Decimal("0")
    for it in items:
        it.sub_total = it.product.price * it.quantity
        total += it.sub_total

    counter = sum(it.quantity for it in items)

    return render(request, "cart/basket.html", {
        "cart_items": items,
        "total": total,
        "counter": counter,
    })

