from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    """
    Get the current cart_id from the session, or create one if it doesn't exist.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """
    Add a product to the shopping cart.
    """
    # Use get_object_or_404 so you don't get a crash if product_id is invalid
    product = get_object_or_404(Product, pk=product_id)

    # Get or create the cart tied to this session
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # Get or create the CartItem
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

    if not created:
        # Item already exists in cart → increment quantity if stock allows
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        # else do nothing (can also raise error if you want)
    else:
        cart_item.quantity = 1

    cart_item.save()
    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    """
    Display the cart and calculate totals.
    """
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        cart_items = []

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
    })
