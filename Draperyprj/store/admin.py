from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "description","stock")

admin.site.register(Product,ProductAdmin)

# Register your models here
