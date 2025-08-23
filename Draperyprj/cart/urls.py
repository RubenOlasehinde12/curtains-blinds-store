from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<uuid:product_id>/", views.add_cart, name="add_cart"),
    path("decrement/<uuid:product_id>/", views.decrement_cart, name="decrement_cart"),
    path("remove/<uuid:product_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("clear/", views.clear_cart, name="clear_cart"),
    path("basket/", views.basket, name="basket"),

]
