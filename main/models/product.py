from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField()
    images = models.JSONField(default=list)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.FloatField()
    sold = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2)
    view = models.IntegerField()
    # promotion = models.ForeignKey(
    #     "Promotion",
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name="products",
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=128)
    product_id = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_images", null=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
