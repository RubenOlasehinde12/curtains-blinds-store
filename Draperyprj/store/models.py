import uuid 
from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True,
        default=uuid.uuid4,
        editable=False)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={"pk": self.id})