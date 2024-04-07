from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from user.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from user.serializers import LoginSerializer
from django.contrib.auth import logout


class RegisterView(views.APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                refresh = RefreshToken.for_user(serializer.instance)

                return Response(
                    {
                        "message": "Đăng ký thành công!",
                        "data": {
                            "user": serializer.data,
                            "expires": 604800,
                            "expires_refresh_token": 8640000,
                            "refresh_token": str(refresh),
                            "access_token": str(refresh.access_token),
                        },
                    },
                    status=201,
                )
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response(
                {"message": "Internal Server Error"},
                status=500,
            )


class LoginView(views.APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data.get("user")
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Đăng nhập thành công!",
                        "data": {
                            "user": {
                                "email": user.email,
                                "name": user.name,
                            },
                            "expires": 604800,
                            "expires_refresh_token": 8640000,
                            "refresh_token": str(refresh),
                            "access_token": str(refresh.access_token),
                        },
                    },
                    status=200,
                )
            else:
                return Response(serializer.errors, status=400)
        except ValidationError as e:
            return Response(
                {"message": str(e)},
                status=400,
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "Internal Server Error"},
                status=500,
            )


class LogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"message": "Missing refresh token"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)

            return Response({"message": "Đăng xuất thành công!"}, status=200)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=500)
