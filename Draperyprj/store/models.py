# store/models.py
import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, blank=True, related_name="products")
    product_image = models.ImageField(upload_to="product_images/", blank=True)

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.product.product_name} — {self.rating}★ by {self.name}"
