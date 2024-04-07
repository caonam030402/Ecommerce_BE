from user.models import Role
from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_name(self, value):
        """
        Check if the name already exists in the database.
        """
        if User.objects.filter(name=value).exists():
            raise ValidationError("Name must be unique.")
        return value

    def create(self, validated_data):
        user = User(
            name=validated_data["name"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
        )

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not check_password(password, user.password):
                    raise ValidationError("Invalid email or password.")
                data["user"] = user
            else:
                raise ValidationError("Invalid email or password.")
        else:
            raise ValidationError("Email and password are required.")

        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "date_of_birth",
            "address",
            "roles",
            "avatar",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        return {key: value for key, value in data.items() if value is not None}
