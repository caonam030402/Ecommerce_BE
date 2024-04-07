from django.urls import path
from main.views.purchase import PurchaseAPIView

purchaseBaseUrl = "purchases"

urlpatterns = [
    path("add-to-cart/", PurchaseAPIView.as_view(), name="add-to-cart"),
    path(
        "",
        PurchaseAPIView.as_view(),
        name="get_user_purchase",
    ),
    path("delete_purchase/", PurchaseAPIView.as_view(), name="delete_purchase"),
    path("buy_products/", PurchaseAPIView.as_view(), name="buy_product"),
    path("update_purchase/", PurchaseAPIView.as_view(), name="update_purchase"),
    path(
        "",
        PurchaseAPIView.as_view(),
        name="get_purchases_with_param",
    ),
]
