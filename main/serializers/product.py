from rest_framework import serializers
from main.models.product import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "image",
            "images",
            "category",
            "description",
            "rating",
            "sold",
            "price",
            "quantity",
            "price_before_discount",
            "view",
            "promotion",
            "created_at",
            "updated_at",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "image",
            "created_at",
            "updated_at",
            "products",
        )
