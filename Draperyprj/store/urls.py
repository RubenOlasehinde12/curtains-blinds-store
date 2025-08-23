from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView, SearchResultsListView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),    
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),

    path("contact/", views.contact_page, name="contact"),
    path("about/", views.about_page, name="about"),

    path("reviews/", views.reviews_list, name="reviews_list"),
    path("<uuid:pk>/review/", views.add_review, name="add_review"),
    
    path("manager/", views.manager_menu, name="manager_menu"),
    path("manager/products/", views.manager_products, name="manager_products"),
    path("manager/products/create/", views.manager_product_create, name="manager_product_create"),
    path("manager/products/<uuid:pk>/edit/", views.manager_product_update, name="manager_product_update"),
    path("manager/products/<uuid:pk>/delete/", views.manager_product_delete, name="manager_product_delete"),
]





