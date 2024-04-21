from django.db import models
from django.conf import settings
from main.models.product import Product


class Purchase(models.Model):
    BUY_STATUS_CHOICES = (
        (0, "Status 0"),
        (-1, "Status -1"),
        (1, "Status 1"),
        (2, "Status 2"),
        (3, "Status 3"),
        (4, "Status 4"),
        (5, "Status 5"),
    )

    buy_count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=BUY_STATUS_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]
