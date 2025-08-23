from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import CheckoutForm

try:
    from cart.models import Cart, CartItem
except Exception:
    Cart = None
    from cart.models import CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def _session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _to_cents(amount):
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount or 0))
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def _load_cart_items(request):
    sk = _session_key(request)
    if Cart is not None:
        try:
            cart = Cart.objects.get(cart_id=sk)
            return list(CartItem.objects.filter(cart=cart).select_related("product"))
        except Exception:
            pass
    try:
        return list(CartItem.objects.filter(cart_id=sk).select_related("product"))
    except Exception:
        pass
    try:
        return list(CartItem.objects.filter(session_key=sk).select_related("product"))
    except Exception:
        return []

def checkout(request):
    cart_items = _load_cart_items(request)
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    subtotal = Decimal("0.00")
    for ci in cart_items:
        ci.sub_total = ci.product.price * ci.quantity
        subtotal += ci.sub_total

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # server-side shipping & coupon
            method = form.cleaned_data["shipping_method"]
            shipping_cost = Decimal("0.00") if method == "standard" else Decimal("6.99")

            code = (form.cleaned_data["coupon"] or "").strip().upper()
            discount = (subtotal * Decimal("0.10")).quantize(Decimal("0.01")) if code == "SAVE10" else Decimal("0.00")

            total = (subtotal + shipping_cost - discount).quantize(Decimal("0.01"))
            if total <= 0:
                messages.error(request, "Total must be greater than €0.00.")
                return redirect("cart:cart_detail")

            try:
                # one line item (your existing pattern)
                session = stripe.checkout.Session.create(
                    mode="payment",
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": "eur",
                            "product_data": {"name": "Cart total"},
                            "unit_amount": _to_cents(total),
                        },
                        "quantity": 1,
                    }],
                    payment_intent_data={"description": "Online Shop - New Order"},
                    success_url=request.build_absolute_uri(reverse("store:product_list")),
                    cancel_url=request.build_absolute_uri(reverse("orders:checkout")),
                )
                return redirect(session.url, code=303)
            except Exception as e:
                messages.error(request, f"Stripe error: {e}")
        # invalid form falls through to render with errors
    else:
        initial = {"email": getattr(request.user, "email", "")}
        form = CheckoutForm(initial=initial)

    # show page (form + items + server subtotal)
    return render(request, "orders/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": subtotal,  # base subtotal; template can show live calc if you want
    })
