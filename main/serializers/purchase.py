from rest_framework import serializers
from main.models.purchase import Purchase
from main.serializers.product import ProductSerializer
from user.serializers import UserSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "buy_count",
            "price",
            "price_before_discount",
            "status",
            "user",
            "product",
        ]
