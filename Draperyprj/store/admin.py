from django.contrib import admin
<<<<<<< HEAD
from .models import Product, Category
=======
from .models import Product
>>>>>>> 152faf7e524f2c4e4a1f15d1045c5adf668ec08c

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "price", "description","stock")

admin.site.register(Product,ProductAdmin)
<<<<<<< HEAD
admin.site.register(Category)
=======
>>>>>>> 152faf7e524f2c4e4a1f15d1045c5adf668ec08c

# Register your models here
