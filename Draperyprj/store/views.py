from django.views.generic import ListView, DetailView
from .models import Product
from django.db.models import Q

# Create your views here
class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'store/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'store/product_detail.html'

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(product_name__icontains=query)
        )