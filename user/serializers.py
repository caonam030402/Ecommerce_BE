from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_name(self, value):
        if User.objects.filter(name=value).exists():
            raise serializers.ValidationError({"email": "Name must be unique."})
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    INVALID_CREDENTIALS_ERROR = {"email": "Invalid email or password."}

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(self.INVALID_CREDENTIALS_ERROR)

            if not check_password(password, user.password):
                raise serializers.ValidationError(self.INVALID_CREDENTIALS_ERROR)

            data["user"] = user
        else:
            raise serializers.ValidationError(
                {"email": "Email and password are required."}
            )

        return data
