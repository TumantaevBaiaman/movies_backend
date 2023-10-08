from django.contrib.auth.hashers import make_password

from django.contrib.auth import password_validation
from rest_framework import serializers

from apps.users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[password_validation.validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "password",
            "password2",
        )

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Пароли не совпадают.")

        password_validation.validate_password(data.get('password'))

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "username",
            "is_admin",
            "is_activ",
        )


class ResetChangePasswordSerializer(serializers.Serializer): # noqa
    new_password = serializers.CharField(required=True)


class LoginUserSerializer(serializers.ModelSerializer): # noqa

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

