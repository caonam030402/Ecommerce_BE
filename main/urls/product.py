from django.urls import path, include
from main.views.product import CategoryAPIView
from main.views.product import ProductViewAPI
from main.views.product import ProductDetailViewAPI

urlpatterns = [
    path("category/", CategoryAPIView.as_view(), name="categorys"),
    path("products/", ProductViewAPI.as_view(), name="products"),
    path(
        "products/<str:product_id>/",
        ProductDetailViewAPI.as_view(),
        name="product-detail",
    ),
]
