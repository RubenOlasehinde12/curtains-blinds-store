from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "price", "description", "stock", "categories", "product_image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


# store/forms.py
from django import forms
from .models import Review, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ReviewCreateForm(ReviewForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta(ReviewForm.Meta):
        fields = ["product", "name", "rating", "comment"]
