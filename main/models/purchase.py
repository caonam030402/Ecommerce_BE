from django.db import models
from user.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
