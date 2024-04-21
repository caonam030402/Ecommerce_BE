from django.urls import path, include
from user.views import RegisterView, LoginView, UserView
from user.views import LogoutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout/"),
    path("me/", UserView.as_view(), name="me"),
    path("user/", UserView.as_view(), name="user"),
]
