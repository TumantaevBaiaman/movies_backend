from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.users.logic import create_user_with_tokens
from apps.users.models import User
from apps.users.serializers import UserRegisterSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return create_user_with_tokens(request.data)

