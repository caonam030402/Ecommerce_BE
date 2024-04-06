from django.db import models
from django.utils import timezone


class PromotionTimeSlots(models.Model):
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()


class Promotion(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.IntegerField()
    quantity = models.IntegerField()
    time_slot = models.ForeignKey("PromotionTimeSlots", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="promotions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
