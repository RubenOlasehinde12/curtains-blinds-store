from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm
from .decorators import staff_required


# -----------------------
# Public product views
# -----------------------
class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.all().prefetch_related("categories")
        cat = self.request.GET.get("category", "").strip()
        if cat:
            qs = qs.filter(categories__name__iexact=cat).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_category"] = self.request.GET.get("category", "").strip()
        return ctx


def home(request):
    products = Product.objects.all()[:8]   # first 8
    return render(request, "home.html", {"products": products})


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/product_detail.html"


class SearchResultsListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/search_results.html"

    def get_queryset(self):
        query = (self.request.GET.get("q") or "").strip()
        if not query:
            return Product.objects.none()
        return Product.objects.filter(Q(product_name__icontains=query))

# Manager views (staff)

@login_required
@staff_required
def manager_menu(request):
    return render(request, "store/manager/manager_menu.html")


@login_required
@staff_required
def manager_products(request):
    products = Product.objects.all().order_by("product_name")
    return render(request, "store/manager/manager_products.html", {"products": products})


@login_required
@staff_required
def manager_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("store:manager_products")  # FIXED name
    else:
        form = ProductForm()
    return render(request, "store/manager/manager_product_form.html", {"form": form, "mode": "Create"})


@login_required
@staff_required
def manager_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("store:manager_products")
    else:
        form = ProductForm(instance=product)
    return render(request, "store/manager/manager_product_form.html", {"form": form, "mode": "Update", "product": product})


@login_required
@staff_required
def manager_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("store:manager_products")
    return render(request, "store/manager/manager_product_confirm_delete.html", {"product": product})



def login_redirect(request):
    if request.user.is_staff:
        return redirect("store:manager_menu")
    return redirect("home")


def contact_page(request):
    return render(request, "store/contact.html")


def about_page(request):
    return render(request, "store/about.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm, ReviewCreateForm
from .models import Review, Product

def reviews_list(request):
    if request.method == "POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Review submitted.")
            return redirect("store:reviews_list")
    else:
        form = ReviewCreateForm()

    reviews = Review.objects.select_related("product").all()[:50]
    return render(request, "store/reviews.html", {"form": form, "reviews": reviews})

def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                product=product,
                name=form.cleaned_data["name"],
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
            )
            messages.success(request, "Review added.")
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm()
    return render(request, "store/review_form.html", {"form": form, "product": product})
