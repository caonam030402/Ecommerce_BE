from django.urls import path, include
from main.views.product import CategoryAPIView

urlpatterns = [
    path("category/", CategoryAPIView.as_view(), name="categorys"),
]
