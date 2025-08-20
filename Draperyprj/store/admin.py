from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "description","stock")

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)

# Register your models here
