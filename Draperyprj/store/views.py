from django.views.generic import ListView, DetailView
from .models import Product
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here
class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.all().prefetch_related("categories")
        cat = self.request.GET.get("category", "").strip()  # ← from query string
        if cat:
            qs = qs.filter(categories__name__iexact=cat).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_category"] = self.request.GET.get("category", "").strip()
        return ctx

    def home(request):
         products = Product.objects.all()[:8]   # first 8, lab-style
         return render(request, "home.html", {"products": products})

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = 'store/product_detail.html'

class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/search_results.html'
    queryset = Product.objects.filter(product_name__icontains="blinds")

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(product_name__icontains=query)
        )

