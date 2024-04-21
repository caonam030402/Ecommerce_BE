from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from user.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from user.serializers import LoginSerializer
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from user.models import User
from rest_framework import status
from user.serializers import UserSerializer
from datetime import datetime
from utils.helpers import custom_response


class RegisterView(views.APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                refresh = RefreshToken.for_user(serializer.instance)

                return custom_response(
                    "Đăng ký thành công!",
                    {
                        "user": serializer.data,
                        "expires": 604800,
                        "expires_refresh_token": 8640000,
                        "refresh_token": "Bearer " + str(refresh),
                        "access_token": "Bearer " + str(refresh.access_token),
                    },
                    200,
                )

            else:
                return custom_response(
                    "Lỗi",
                    {
                        "email": "Email hoặc user đã tồn tại",
                    },
                    422,
                )

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
                user_data = UserSerializer(user).data

                return custom_response(
                    "Đăng nhập thành công",
                    {
                        "user": user_data,
                        "expires": 604800,
                        "expires_refresh_token": 8640000,
                        "refresh_token": "Bearer " + str(refresh),
                        "access_token": "Bearer " + str(refresh.access_token),
                    },
                    200,
                )

            else:
                data = {
                    "password": "Email hoặc password không đúng",
                }
                return custom_response("Lỗi", data, 422)

        except ValidationError as e:
            print(e)

        except Exception as e:
            print(e)
            return Response(
                {"message": "Internal Server Error"},
                status=500,
            )


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user.id

            if not user:
                return Response({"message": "Missing refresh token"}, status=400)

            logout(request)

            return Response({"message": "Đăng xuất thành công!"}, status=200)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=500)


class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user_id = request.user.id

            user = User.objects.get(id=user_id)

            if "date_of_birth" in request.data:
                iso_date_str = request.data["date_of_birth"]
                formatted_date = datetime.strptime(
                    iso_date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%Y-%m-%d")
                request.data["date_of_birth"] = formatted_date

            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data={
                        "message": "Cập nhật thành công",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=500)

    def get(self, request):
        try:
            user_id = request.user.id

            user = User.objects.get(id=user_id)

            serializer = UserSerializer(user).data

            return Response(
                data={
                    "message": "Lấy người dùng thành công",
                    "data": serializer,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"message": "Internal Server Error"}, status=500)
