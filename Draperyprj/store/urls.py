from django.urls import path
from .views import ProductListView, ProductDetailView, SearchResultsListView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),    
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]

