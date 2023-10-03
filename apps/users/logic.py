from datetime import datetime

from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.users.serializers import UserRegisterSerializer


def create_user_and_cart(data):
    serializer = UserRegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return None, user
    return serializer.errors, None


def create_tokens(user):
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    access_token_expiration = (datetime.utcnow() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    refresh_token_expiration = (datetime.utcnow() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

    return {
        'access': str(access_token),
        'refresh': str(refresh_token),
        'access_token_expiration': access_token_expiration,
        'refresh_token_expiration': refresh_token_expiration,
    }


def create_user_with_tokens(data):
    err, user = create_user_and_cart(data)
    if user:
        tokens = create_tokens(user)
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "phone": user.phone,
            "is_admin": user.is_admin,
        }
        response_data = {
            'detail': 'Вы успешно зарегистрированы!',
            'user': user_data,
            **tokens,
        }

        return Response(response_data, status=201)
    return Response(err, status=400)
