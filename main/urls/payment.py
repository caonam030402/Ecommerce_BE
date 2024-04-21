from django.urls import path

from main.views.payment import PaymentAPIView

urlpatterns = [
    path("create-payment-url/", PaymentAPIView.as_view(), name="create_payment_url"),
    path("vnpay-return/", PaymentAPIView.as_view(), name="vnp_return"),
]
