from django.urls import include, path
from .product import urlpatterns as product_urls
from .purchase import urlpatterns as purchases_urls

urlpatterns = [
    path("api/v1/", include(product_urls)),
    path("api/v1/purchases/", include(purchases_urls)),
]
