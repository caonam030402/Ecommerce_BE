from django.urls import include, path
from .product import urlpatterns as product_urls

urlpatterns = [
    path("api/v1/", include(product_urls)),
]
